from collections import Counter
from google.cloud import vision
from google.api_core import exceptions

def analyze_store_shelf(image_path: str, confidence_threshold: float = 0.8):
    """
    Detects and counts items in an image, filtering by confidence and
    extracting text from labels.

    Args:
        image_path (str): The path to the local image file.
        confidence_threshold (float): Minimum score for valid detection.
    """
    client = vision.ImageAnnotatorClient()

    try:
        print(f"Reading image from: {image_path}")
        with open(image_path, "rb") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File not found at '{image_path}'")
        return
    
    image = vision.Image(content=content)

    features = [
        {"type_": vision.Feature.Type.OBJECT_LOCALIZATION},
        {"type_": vision.Feature.Type.TEXT_DETECTION},
    ]

    try:
        print("Sending request to Google Cloud Vision API...")
        response = client.annotate_image({"image": image, "features": features})
        print("API request complete.")
    except exceptions.GoogleAPICallError as e:
        print(f"API error occurred: {e}")
        return

    all_objects = response.localized_object_annotations
    filtered_objects = [obj for obj in all_objects if obj.score >= confidence_threshold]

    print(f"\nFound {len(all_objects)} total objects. Kept {len(filtered_objects)} after applying {confidence_threshold:.0%} confidence threshold.")

    if filtered_objects:
        item_counts = Counter(obj.name for obj in filtered_objects)
        print("\n--- Inventory Summary ---")
        for item, count in item_counts.items():
            print(f"Item: {item}, Quantity: {count}")
        print("------------------------\n")
    else:
        print("No items detected with sufficient confidence.")

    texts = response.text_annotations
    if texts:
        print("--- Detected Text on Products ---")
        print(texts[0].description.replace('\n', ' | '))
        print("-------------------------------\n")
    else:
        print("No text detected on the products.")



if __name__ == "__main__":
    
    image_file = "C:/Users/Tejas/Desktop/programming/code/aiml/LedgerLens/AI/ObjectDetection/unnamed.png"
    
    analyze_store_shelf(image_file, confidence_threshold=0.8)
        