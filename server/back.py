from flask import Flask, request, jsonify
from PIL import Image
from pillow_heif import register_heif_opener
from tensorflow.keras.models import load_model
import numpy as np

# Register HEIF opener with Pillow (assuming model works with RGB images)
register_heif_opener()

# Load your pre-trained model
model = load_model("final_model.h5")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, world!"

@app.route("/predict", methods=["POST", 'GET'])
def predict_cleanliness():
  # Get image data from request
#   if "image" not in request.files:
#       return jsonify({"error": "No image uploaded"}), 400
#   image_file = request.files["image"]

  try:
      # Open image using Pillow (handles HEIF)
      img = Image.open('messy_classifier/IMG_0944.HEIC')

      img = img.convert('RGB')  # Ensure RGB mode for model compatibility
      img = img.resize((224, 224))
      img_data = np.array(img)
      img_data = img_data.astype("float32") / 255.0
      img_data = np.expand_dims(img_data, axis=0)

      # Make prediction using the model
      pred = model.predict(img_data)[0][0]
      if pred > 0.9:  # Adjust threshold as needed
          prediction = "Messy"
      else:
          prediction = "Clean"

      return jsonify({"prediction": prediction})
  except Exception as e:
      print(f"Error processing image: {e}")
      return jsonify({"error": f"Error processing image : {e}"}), 500

if __name__ == "__main__":
  app.run(debug=True)
