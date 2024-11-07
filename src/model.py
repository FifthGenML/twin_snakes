import requests
import base64
import io
from PIL import Image
import numpy as np
from src.utils import score

def get_prediction_probs(image_np):

    image = Image.fromarray(image_np.astype(np.uint8))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    response = score(img_str)
    return response['output']