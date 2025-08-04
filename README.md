# Emergency Lighting Detection from Construction Blueprints

## Overview

This project implements an AI vision pipeline to automate the detection and analysis of emergency lighting fixtures from multi-sheet electrical drawing PDFs. The solution processes PDF blueprints, extracts key information from legends and schedules, and uses image processing to visually identify emergency light fixtures on floor plans. The final output is a structured JSON report that summarizes the detected emergency lighting systems, their specifications, and their locations on the blueprints.

## Project Concept

The pipeline is designed to address a common challenge in construction planning: manually sifting through complex technical drawings to identify specific components. Our solution automates this process using a multi-faceted approach:

1.  **PDF to Image Conversion**: The multi-page PDF is converted into a series of high-resolution images to enable visual analysis and OCR.
2.  **OCR and Data Extraction**: Optical Character Recognition (OCR) is performed on each image to extract all text. This raw text is then intelligently parsed to isolate key sections such as the "Lighting Fixture Schedule" and "General Notes".
3.  [cite_start]**Computer Vision for Detection**: A computer vision model applies image processing techniques to the floor plan images to detect shaded rectangular areas, which represent emergency light fixtures[cite: 87]. This process filters out non-relevant elements like title blocks and page numbers to ensure accuracy.
4.  **Information Synthesis**: The extracted text data (e.g., fixture type, wattage, description) is correlated with the visually detected objects. This allows the system to not only count the total number of emergency lights but also link them to their specific technical specifications. The final output is a comprehensive JSON report.

## Folder Structure

The project is organized into a modular structure for clarity and maintainability:

<img width="324" height="346" alt="image" src="https://github.com/user-attachments/assets/63d2b9be-ed77-4df4-8a38-dfc58f3a088b" />


## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/vision_takeoff.git](https://github.com/your-username/vision_takeoff.git)
    cd vision_takeoff
    ```

2.  **Set up a virtual environment** (recommended to avoid dependency conflicts):
    ```bash
    conda create --name my_vision_env python=3.10
    conda activate my_vision_env
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` includes pinned versions to ensure compatibility, especially with `numpy` and `opencv-python`.*

4.  **Install Tesseract OCR:** This project requires the Tesseract executable, as `pytesseract` is just a wrapper.
    * Download and install it from [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki).
    * **Crucially**, ensure the Tesseract installation path is added to your system's PATH environment variable during installation.
## API Endpoints and Usage

The project includes a web API (using Flask/FastAPI) designed for deployment on platforms like Render. It handles PDF processing in the background to ensure a smooth user experience.

* **`POST /blueprints/upload`**: Uploads a PDF file and initiates the analysis. It returns a job ID to track the process.
* **`GET /blueprints/result?pdf_name=...`**: Retrieves the final JSON report once processing is complete.

### Local Demonstration

To run the API locally and test it, follow these steps:
1.  Run the main application from the project root:
    ```bash
    python src/main.py data/PDF.pdf
    ```
    *This will generate the output files in the `output/` directory.*

2.  You can then inspect the generated `report_PDF.json` and the visualization images.

## Annotated Example

The following image shows an example of a detected emergency light on a blueprint. The red box highlights a shaded area, which according to the provided legend, symbolizes a light fixture connected to the emergency lighting system.

<img width="498" height="350" alt="image" src="https://github.com/user-attachments/assets/27045170-58df-4c0a-9146-37e490237234" />


## Postman Collection

A Postman collection is included to demonstrate the API's functionality. You can import the collection to easily test the `POST /upload` and `GET /result` endpoints.

* **Public Postman Link**: [Your Postman link here]
* **JSON File**: `postman_collection.json` (if you prefer to host it in the repo)






