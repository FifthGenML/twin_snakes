import sys
import os
import random
import numpy as np
from PIL import Image
from src.utils import perturb, crossover, mutate, tournament_selection
from src.model import get_prediction_probs
import src.config as config
from src.artifact import create_artifact

def fitness(probs, target_class):
    target_prob = next((prob[0] for prob in probs if prob[1].lower() == target_class), 0)
    return target_prob

def init_population(original_image, pop_size, pert_mag, pert_pixels):
    population = []
    for _ in range(pop_size):
        image = original_image.copy()
        perturb(image, pert_mag, pert_pixels)
        population.append(image)
    return population

def genetic_attack(original_image):
    population = init_population(original_image, config.POP_SIZE, config.PERT_MAG, config.PERT_PIXELS)
    
    for gen in range(config.GENERATIONS):
        scores = []
        target_probabilities = []
        highest_prob_labels = []
        
        for ind in population:
            probs = get_prediction_probs(ind)
            score = fitness(probs, config.TARGET_CLASS)
            scores.append(score)
            target_prob = next((prob[0] for prob in probs if prob[1].lower() == config.TARGET_CLASS), 0)
            target_probabilities.append(target_prob)
            highest_prob_label = max(probs, key=lambda x: x[0])
            highest_prob_labels.append(highest_prob_label)
        
        best_score = max(scores)
        best_individual_index = scores.index(best_score)
        best_target_prob = target_probabilities[best_individual_index]
        best_highest_label, best_highest_prob = highest_prob_labels[best_individual_index][1], highest_prob_labels[best_individual_index][0]
        
        print(f"Generation {gen+1} - Best score: {best_score}")
        print(f"  Target class '{config.TARGET_CLASS}' prob: {best_target_prob}")
        print(f"  Highest probability label: '{best_highest_label}' with prob: {best_highest_prob}")
        
        if best_target_prob >= config.TARGET_THRESHOLD or best_highest_label.lower() == config.TARGET_CLASS.lower():
            print(f"Target achieved with class '{config.TARGET_CLASS}' probability {best_target_prob} in generation {gen + 1}")
            return population[best_individual_index]
        
        parents = tournament_selection(population, scores, config.K, config.POP_SIZE)
        
        children = []
        while len(children) < config.POP_SIZE:
            parent1, parent2 = random.sample(parents, 2)
            child = crossover(parent1, parent2)
            if random.uniform(0, 1) < config.RATE_MUT:
                mutate(child, config.MUT_MAG, config.MUT_PIXELS)
            children.append(child)
        
        population = children
    
    print("Max generations reached without achieving target.")
    return population[scores.index(max(scores))]

def main():

    image_path = sys.argv[1] if len(sys.argv) > 1 else create_artifact()
    
    if not image_path.lower().endswith('.png'):
        print("Error: The input image must be a PNG file.")
        sys.exit(1)
    
    try:
        original_image = np.array(Image.open(image_path))
        adversarial_image = genetic_attack(original_image)
        adversarial_image_pil = Image.fromarray(adversarial_image.astype(np.uint8))
        adversarial_image_pil.save("adversarial_image.png")
    except Exception as e:
        print(f"Error loading image: {e}")

if __name__ == "__main__":
    main()