from flask import Flask, request, jsonify, render_template
from collections import Counter
from google.cloud import vision
from google.api_core import exceptions
import os

app = Flask(__name__)

# It's best practice to set the GOOGLE_APPLICATION_CREDENTIALS environment
# variable in your terminal before running the app.
# Example (Linux/macOS): export GOOGLE_APPLICATION_CREDENTIALS="/path/to/key.json"
# Example (Windows): set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\key.json"

@app.route("/", methods=["GET"])
def index():
    """Serves the main page."""
    return render_template('home.html')

def analyze_store_shelf(image_content: bytes, confidence_threshold: float = 0.8) -> dict:
    """
    Analyzes an image of a store shelf using Google Cloud Vision API.

    Args:
        image_content: The binary content of the image file.
        confidence_threshold: The minimum score for an object to be included.

    Returns:
        A dictionary containing the analysis results.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    features = [
        {"type_": vision.Feature.Type.OBJECT_LOCALIZATION},
        {"type_": vision.Feature.Type.TEXT_DETECTION},
    ]

    try:
        response = client.annotate_image({"image": image, "features": features})
    except exceptions.GoogleAPICallError as e:
        return {"error": f"Google API Error: {e.message}"}

    all_objects = response.localized_object_annotations
    filtered_objects = [obj for obj in all_objects if obj.score >= confidence_threshold]
    item_counts = Counter(obj.name for obj in filtered_objects)

    texts = response.text_annotations
    detected_text = texts[0].description.replace('\n', ' | ') if texts else "No text detected."

    result = {
        "total_objects_detected": len(all_objects),
        "objects_above_threshold": len(filtered_objects),
        "item_summary": dict(item_counts),
        "detected_text": detected_text
    }
    return result

@app.route('/analyze', methods=['POST'])
def analyze_image_route():
    """Handles the image upload and returns the analysis as JSON."""
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        image_content = file.read()
        confidence = float(request.form.get('confidence_threshold', 0.8))

        if not 0.0 <= confidence <= 1.0:
            return jsonify({"error": "Confidence threshold must be between 0.0 and 1.0"}), 400

        result = analyze_store_shelf(image_content, confidence)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
