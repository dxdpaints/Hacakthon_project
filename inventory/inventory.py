import cv2
import easyocr
import numpy as np
import PIL
from PIL import Image, PngImagePlugin
import google.generativeai as genai
  # Import for Gemini Pro Vision (if API key provided)
from pillow_heif import register_heif_opener
register_heif_opener()


# Configure Gemini Pro Vision API (if using)
try:
  genai.configure(api_key="AIzaSyAeItfWvdaFYYF3AxHAbKQOGyAUIwngzlQ")  # Replace with your API key if using Gemini
  model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
  print(f"Error configuring Gemini Pro Vision: {str(e)}")
  model = None  # Set model to None if Gemini configuration fails

def extract_bathroom_inventory(image_path):
  """
  Extracts potential inventory items from a bathroom image using Gemini Pro Vision (if available) and text detection.

  Args:
      image_path (str): Path to the bathroom image file.

  Returns:
      list: List of potential inventory items found in the image.
  """

  # Read the image
  img = Image.open('IMG_0915.HEIC')
  # print(type(img))

  # Convert OpenCV image to RGB format (PIL expects RGB)
  # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

 # Create a PIL Image object from the RGB image
  # img_rgb = Image.fromarray(img)

  # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB format

  # Use Gemini Pro Vision for object detection (if configured)
  if model:
    try:
      results = model.generate_content([img, "List all the inventory items in the image. Inventory items include towels, hand napkins, soap containers, shampoo containers."], stream=True)
      results.resolve()
      inventory_text = results.text
    except Exception as e:
      print(f"Error using Gemini Pro Vision: {str(e)}")
      inventory_text = ""  # Empty string if Gemini fails
    print('inside if model')
  else:
    inventory_text = ""  # Empty string if Gemini is not configured

  # Use EasyOCR for text detection as a fallback
  # reader = easyocr.Reader(['en'], gpu=False)
  # results = reader.readtext(img_rgb)
  # text = " ".join([result[1] for result in results])  # Combine recognized text
  print(inventory_text)

  # Define a list of common bathroom inventory items for filtering
  bathroom_items = ["towel", "shampoo", "soap", "conditioner", "toothbrush", "toothpaste", "razor", "floss", "hairdryer", "comb", "brush", "deodorant", "makeup", "lotion", "toilet paper", "bath mat", "shower curtain", "bathrobe", "scale"]

  # Extract potential inventory items from the text and Gemini output (case-insensitive)
  potential_items = [item.lower() for item in (inventory_text + " ").lower().split() if item.lower() in bathroom_items]
  filtered_items = list(set(potential_items))  # Remove duplicates


  return filtered_items

# Example usage
image_path = "1.HEIC"

bathroom_inventory = extract_bathroom_inventory(image_path)
if bathroom_inventory:
  print("Potential Bathroom Inventory:")
  for item in bathroom_inventory:
    print(item)
else:
  print("No inventory items found in the image.")