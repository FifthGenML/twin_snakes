import numpy as np
import requests
import src.config as config
from PIL import Image
import random

def query(input_data):
    try:
        if isinstance(input_data, bytes):
            input_data = input_data.decode()
        response = requests.post(
            f"{config.CHALLENGE_URL}/score",
            headers={"X-API-Key": config.CRUCIBLE_API_KEY},
            json={"data": input_data},
        )
        return response.json()
    except TypeError as e:
        if "Object of type builtin_function_or_method is not JSON serializable" in str(e):
            raise e
        else:
            raise e

def score(reference):
    try:
        result = query(reference)
    except TypeError as e:
        if "Object of type builtin_function_or_method is not JSON serializable" in str(e):
            result = query(reference.decode())
            print(result)
        else:
            raise e
    return result


def perturb(image, magnitude, pixels):
    flat_image = image.reshape(-1, 3).astype(np.float32)
    num_pixels = flat_image.shape[0]
    pixels = min(pixels, num_pixels)
    indices = np.random.choice(num_pixels, pixels, replace=False)
    perturbation = np.random.normal(0, magnitude * 255, (pixels, 3))
    flat_image[indices] += perturbation
    np.clip(flat_image, 0, 255, out=flat_image)
    image[:] = flat_image.astype(np.uint8).reshape(image.shape)

def crossover(parent1, parent2):
    child = parent1.copy()
    child[::2] = parent2[::2]
    return child

def mutate(image, mut_mag, mut_pixels):
    perturb(image, mut_mag, mut_pixels)

def tournament_selection(population, scores, k, pop_size):
    new_population = []
    for _ in range(pop_size):
        selected = random.sample(range(len(population)), k)
        best_index = max(selected, key=lambda i: scores[i])
        new_population.append(population[best_index])
    return new_population

def rescale_image(image_np, scale_factor=0.5):

    image = Image.fromarray(image_np.astype(np.uint8))
    small_image = image.resize(
        (int(image.width * scale_factor), int(image.height * scale_factor)),
        Image.LANCZOS
    )
    resized_back = small_image.resize((image.width, image.height), Image.LANCZOS)
    small_image_np = np.array(small_image)
    resized_back_np = np.array(resized_back)
    
    return small_image_np, resized_back_np