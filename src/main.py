# import argparse
# import os
# import json
# from pdf_processor import pdf_to_images, extract_text_from_images
# from data_extractor import extract_general_notes, extract_lighting_schedule
# from detector import detect_shaded_emergency_lights

# def process_file(file_path):
#     print(f"Processing file: {file_path}")
    
#     # Step 1 & 2: PDF to Images and OCR
#     images = pdf_to_images(file_path)
#     extracted_texts = extract_text_from_images(images)

#     # Step 3: Parse Static Content
#     all_text = " ".join(extracted_texts)
#     general_notes = extract_general_notes(all_text)
#     lighting_schedule = extract_lighting_schedule(all_text)
    
#     # Store static content for database
#     static_content_db = {
#         "file_name": os.path.basename(file_path),
#         "general_notes": general_notes,
#         "lighting_schedule": lighting_schedule
#     }
    
#     # Step 4: Emergency Lighting Detection
#     all_detected_lights = {}
#     for i, img in enumerate(images):
#         detected_lights = detect_shaded_emergency_lights(img)
#         if detected_lights:
#             all_detected_lights[f"page_{i+1}"] = detected_lights
    
#     # Step 5: Information Linking and Structuring
#     # This part would involve an LLM call or a hardcoded logic
#     # as described in the previous response.
#     # For this CLI, we will perform a simple count.
    
#     # Hardcoded counts based on the lighting schedule
#     count_2x4_emergency = 0
#     count_wallpack_emergency = 0
    
#     for item in lighting_schedule:
#         desc = item.get('DESCRIPTION', '').lower()
#         if 'emergency driver' in desc and '2\' x 4\' recessed led luminaire' in desc:
#             count_2x4_emergency += 1
#         if 'wallpack' in desc and 'photocell' in desc and 'emergency' in desc:
#             count_wallpack_emergency += 1

#     report = {
#         "file_name": os.path.basename(file_path),
#         "emergency_lighting_summary": {
#             "from_schedule_count": {
#                 "2x4_recessed_led_luminaire": count_2x4_emergency,
#                 "wallpack_with_photocell": count_wallpack_emergency,
#             },
#             "detected_lights_on_layouts": all_detected_lights,
#         },
#         "extracted_content": static_content_db
#     }
    
#     output_filename = f"report_{os.path.basename(file_path).replace('.pdf', '.json')}"
#     output_path = os.path.join("output", output_filename)
#     with open(output_path, "w") as f:
#         json.dump(report, f, indent=4)
        
#     print(f"Processing complete. Report saved to {output_path}")

# def main():
#     parser = argparse.ArgumentParser(description="AI Vision Takeoff for Emergency Lighting Detection.")
#     parser.add_argument("file_path", help="Path to the PDF file to process.")
    
#     args = parser.parse_args()
    
#     if not os.path.exists("output"):
#         os.makedirs("output")
        
#     process_file(args.file_path)

# if __name__ == "__main__":
#     main()
# In src/main.py

import argparse
import os
import json
import cv2
import numpy as np
from pdf_processor import pdf_to_images, extract_text_from_images
from data_extractor import (
    extract_general_notes, 
    extract_lighting_schedule,
    count_emergency_lights_from_schedule
)
from detector import detect_shaded_emergency_lights
from PIL import ImageDraw, ImageFont

def draw_bboxes_on_image(image, bboxes):
    """Draws bounding boxes on an image for verification."""
    img_pil = image.copy()
    draw = ImageDraw.Draw(img_pil)
    # Use a solid fill color for the boxes
    fill_color = (255, 0, 0, 100) # Red with some transparency
    
    for bbox in bboxes:
        x1, y1, x2, y2 = bbox['bbox']
        # Draw a semi-transparent rectangle
        draw.rectangle([x1, y1, x2, y2], fill=fill_color, outline=(255, 0, 0), width=2)
    
    return img_pil

def process_file(file_path):
    print(f"Processing file: {file_path}")
    
    # Step 1 & 2: PDF to Images and OCR
    images = pdf_to_images(file_path)
    extracted_texts = extract_text_from_images(images)

    # Step 3: Parse Static Content
    all_text = " ".join(extracted_texts)
    general_notes = extract_general_notes(all_text)
    lighting_schedule = extract_lighting_schedule(all_text)
    
    # Store static content for database
    static_content_db = {
        "file_name": os.path.basename(file_path),
        "general_notes": general_notes,
        "lighting_schedule": lighting_schedule
    }
    
    # Step 4: Emergency Lighting Detection
    all_detected_lights = {}
    for i, img in enumerate(images):
        # We only want to detect lights on floor plan pages.
        # This is a heuristic that may need to be refined.
        if "floor plan" in extracted_texts[i].lower():
            detected_lights = detect_shaded_emergency_lights(img)
            if detected_lights:
                all_detected_lights[f"page_{i+1}"] = detected_lights
                # Visualize the results and save
                visual_img = draw_bboxes_on_image(img, detected_lights)
                visual_img.save(f"output/detected_lights_page_{i+1}.png")
                print(f"Saved visualization for page {i+1}")
    
    # Step 5: Information Linking and Structuring
    emergency_counts = count_emergency_lights_from_schedule(lighting_schedule)

    report = {
        "file_name": os.path.basename(file_path),
        "emergency_lighting_summary": {
            "from_schedule_count": emergency_counts,
            "detected_lights_on_layouts": all_detected_lights,
        },
        "extracted_content": static_content_db
    }
    
    output_filename = f"report_{os.path.basename(file_path).replace('.pdf', '.json')}"
    output_path = os.path.join("output", output_filename)
    with open(output_path, "w") as f:
        json.dump(report, f, indent=4)
        
    print(f"Processing complete. Report saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="AI Vision Takeoff for Emergency Lighting Detection.")
    parser.add_argument("file_path", help="Path to the PDF file to process.")
    
    args = parser.parse_args()
    
    if not os.path.exists("output"):
        os.makedirs("output")
        
    process_file(args.file_path)

if __name__ == "__main__":
    main()