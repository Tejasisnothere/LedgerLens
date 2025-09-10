from flask import Flask, request, jsonify, render_template_string
import tensorflow as tf
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Update this to your actual model path
MODEL_PATH = "C:/Users/Tejas/Desktop/programming/code/aiml/LedgerLens/AI/ObjectDetection/newfoldder/ssd_mobilenet_v2_fpnlite_320x320_coco17_tpu-8/saved_model"

# Load the TensorFlow model
detect_fn = tf.saved_model.load(MODEL_PATH)

# HTML template for the upload page
UPLOAD_PAGE = """
<!doctype html>
<html lang="en">
<head>
  <title>Object Detection Upload</title>
</head>
<body>
  <h1>Upload an image for object detection</h1>
  <form method="POST" action="/detect_items" enctype="multipart/form-data">
    <input type="file" name="image" required>
    <button type="submit">Upload and Detect</button>
  </form>
  {% if results %}
    <h2>Detected Classes:</h2>
    <ul>
      {% for item in results %}
        <li>{{ item }}</li>
      {% endfor %}
    </ul>
  {% endif %}
</body>
</html>
"""

# Dummy label map for demonstration (use actual label map in production)
LABEL_MAP = {
    44: "bottle",
    47: "cup",
    52: "banana",
    53: "apple",
    54: "sandwich",
    55: "orange",
    56: "broccoli",
    57: "carrot",
    58: "hot dog",
    59: "pizza",
    60: "donut",
    61: "cake",
    70: "toothbrush",
    72: "toothpaste",
    73: "shampoo",
    74: "conditioner",
    75: "soap",
    76: "detergent",
    77: "cleaner",
    78: "mop",
    79: "bucket",
    80: "sponge",
    81: "towel",
    82: "napkin",
    83: "paper towel",
    84: "toilet paper",
    85: "tissue",
    86: "band-aid",
    87: "pain reliever",
    88: "cough syrup",
    89: "vitamins",
    90: "bandages",
    91: "first aid kit",
    92: "sunscreen",
    93: "lip balm",
    94: "hand sanitizer",
    95: "air freshener",
    96: "light bulb",
    97: "batteries",
    98: "extension cord",
    99: "flashlight",
    100: "matches",
    101: "lighter",
    102: "candles",
    103: "umbrella",
    104: "raincoat",
    105: "gloves",
    106: "hat",
    107: "scarf",
    108: "sunglasses",
    109: "watch",
    110: "wallet",
    111: "purse",
    112: "backpack",
    113: "laptop",
    114: "tablet",
    115: "smartphone",
    116: "charger",
    117: "headphones",
    118: "earbuds",
    119: "camera",
    120: "tripod",
    121: "memory card",
    122: "power bank",
    123: "keyboard",
    124: "mouse",
    125: "printer",
    126: "ink cartridge",
    127: "notebook",
    128: "pen",
    129: "pencil",
    130: "eraser",
    131: "sharpener",
    132: "stapler",
    133: "paper clips",
    134: "scissors",
    135: "glue",
    136: "tape",
    137: "calculator",
    138: "ruler",
    139: "compass",
    140: "protractor",
    141: "dictionary",
    142: "encyclopedia",
    143: "atlas",
    144: "board game",
    145: "playing cards",
    146: "puzzle",
    147: "toy car",
    148: "doll",
    149: "action figure",
    150: "stuffed animal",
    151: "ball",
    152: "frisbee",
    153: "bat",
    154: "glove",
    155: "helmet",
    156: "knee pads",
    157: "elbow pads",
    158: "skateboard",
    159: "scooter",
    160: "bicycle",
    161: "helmet",
    162: "knee pads",
    163: "elbow pads",
    164: "skateboard",
    165: "scooter",
    166: "roller skates",
    167: "bicycle lock",
    168: "bike pump",
    169: "bike light",
    170: "bike bell",
    171: "bike basket",
    172: "bike rack",
    173: "bike lock",
    174: "bike helmet",
    175: "bike gloves",
    176: "bike shoes",
    177: "bike shorts",
    178: "bike jersey",
    179: "bike water bottle",
    180: "bike repair kit",
    181: "bike tire",
    182: "bike tube",
    183: "bike pump",
    184: "bike chain",
    185: "bike lock",
    186: "bike bell",
    187: "bike light",
    188: "bike basket",
    189: "bike rack",
    190: "bike lock",
    191: "bike helmet",
    192: "bike gloves",
    193: "bike shoes",
    194: "bike shorts",
    195: "bike jersey",
    196: "bike water bottle",
    197: "bike repair kit",
    198: "bike tire",
    199: "bike tube",
    200: "bike pump"
}


@app.route("/", methods=["GET"])
def index():
    return render_template_string(UPLOAD_PAGE)

@app.route("/detect_items", methods=["POST"])
def detect_items():
    if "image" not in request.files:
        return "No image uploaded", 400
    
    file = request.files["image"]
    if file.filename == "":
        return "No image selected", 400

    # Load image
    image = Image.open(file.stream)
    image_np = np.array(image)

    # Add batch dimension
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Perform detection
    detections = detect_fn(input_tensor)

    # Get class IDs and confidence scores
    classes = detections["detection_classes"][0].numpy().astype(int)
    scores = detections["detection_scores"][0].numpy()

    # Filter out detections with low confidence
    threshold = 0.5
    detected_items = []
    for cls, score in zip(classes, scores):
        if score > threshold:
            name = LABEL_MAP.get(cls, f"Class {cls}")
            detected_items.append(f"{name} ({score:.2f})")

    # Render the page with results
    return render_template_string(UPLOAD_PAGE, results=detected_items)

if __name__ == "__main__":
    app.run(debug=True)
