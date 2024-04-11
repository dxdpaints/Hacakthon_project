import cv2
import easyocr
import numpy as np
import PIL
from PIL import Image, PngImagePlugin
import google.generativeai as genai
from pillow_heif import register_heif_opener
register_heif_opener()
import os
from dotenv import load_dotenv

GEMINI_API = os.getenv('GEMINI_API')

try:
  genai.configure(api_key=GEMINI_API)
  model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
  print(f"Error configuring Gemini Pro Vision: {str(e)}")
  model = None

def extract_bathroom_inventory(image_path):
  img = Image.open('IMG_0915.HEIC')

  if model:
    try:
      results = model.generate_content([img, "List all the inventory items in the image. Inventory items include towels, hand napkins, soap containers, shampoo containers."], stream=True)
      results.resolve()
      inventory_text = results.text
    except Exception as e:
      print(f"Error using Gemini Pro Vision: {str(e)}")
      inventory_text = ""
  else:
    inventory_text = ""

    #If we need to detect specific items in the image, we can mention the items in bathroom_items and return the filtered_items 
    bathroom_items = ["towel", "shampoo", "soap", "conditioner", "toothbrush", "toothpaste", "razor", "floss", "hairdryer", "comb", "brush", "deodorant", "makeup", "lotion", "toilet paper", "bath mat", "shower curtain", "bathrobe", "scale"]
    filtered_items = list(set([item.lower() for item in (inventory_text + " ").lower().split() if item.lower() in bathroom_items]))

  return inventory_text

image_path = "1.HEIC"

bathroom_inventory = extract_bathroom_inventory(image_path)
if bathroom_inventory:
  print("Potential Bathroom Inventory:")
  print(bathroom_inventory)
else:
  print("No inventory items found in the image.")

  