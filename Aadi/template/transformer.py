# from transformers import pipeline
# from PIL import Image
# import requests

# # Use a generic ViT model trained on ImageNet
# classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

# from google.colab import files
# uploaded = files.upload()
# img_path = list(uploaded.keys())[0]

# img_url = 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8'  # Replace with the actual URL
# image = Image.open(requests.get(img_url, stream=True).raw)

# image = Image.open(img_path)
# result = classifier(image)
# print(result)

from transformers import pipeline
from PIL import Image

# Load model only once (fast)
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

def predict_image(image_path):

    # Open the uploaded image
    image = Image.open(image_path)

    # Run prediction
    result = classifier(image)

    # Convert result (dict) to readable text
    label = result[0]['label']
    score = round(result[0]['score'] * 100, 2)

    return f"Prediction: {label} ({score}%)"
