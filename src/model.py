
import io
import base64
from PIL import Image
import requests
import numpy as np
from src.utils import score,query

def get_prediction_probs(image_np):
    # Convert numpy array to image
    image = Image.fromarray(image_np.astype(np.uint8))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    response = score(img_str)
    return response['output']