import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from homerate.settings import BASE_DIR, STATIC_ROOT


def is_adult_content(path):
    # Concatenate base path and the relative path
    path = BASE_DIR + path

    # Set the environment variable for the application credential
    key_path = STATIC_ROOT + "/google_vision_key.json"
    print(key_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    # Create an instance of the google vision API
    client = vision.ImageAnnotatorClient()

    # Open the image
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    # Test the image using google API
    image = vision.types.Image(content=content)
    response = client.safe_search_detection(image=image)
    safe = response.safe_search_annotation

    # Check if the image meets adult content minimums
    max_allowed = 3
    adult_content = safe.adult > max_allowed or safe.racy > max_allowed or safe.violence > max_allowed

    # Delete the file if adult content
    if adult_content:
        os.remove(path)

    # Return whether or not the image was adult content
    return adult_content
