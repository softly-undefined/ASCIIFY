from skimage.metrics import structural_similarity as ssim
from scipy.spatial.distance import euclidean
import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# WELCOME TO                                                                     
#        __        ___       _____ _______ _______  ggg@gg____      __  
#       g@@_    _@@NNNNK   _@@MM@@^MM@@NNNFMMN@@NNP @N""""M"^@@_   @@F  
#     _@@N@E   q@B____    @@P`   `   B@      [@E    @R_____   0@_ @@F   
#    _@@__@@    "MMNNN@g @@F         @@      [@E    @@MMMMP    %@@@F    
#   g@BMMMN@L ___    _@@L0@_   _g,   @@      [@E    @0          @@F     
#   @0     0@ ^@@@g@@@NM  M@@@@NM` @@@@@@@ g@@@@@@L @0         @@F      
#           `    ````              ``       `       "`         ``       
# by eric bennett


pixel_size = 100 #the larger this number is, the less characters in the image
image_path = "input-files/eric.png"
output_file = "output_ascii_art.txt"


# Weights- these should add up to 1
# right now I'm only using euclidean distance because using cosine similarity
# completely black and completely white are evaluated as equally 'correct'
euclidean_weight = 1 
cosine_sim_weight = 0


#loads intensity vectors of pixel_size pixelations of the ascii characters
def load_ascii(pixel_size):
    # ASCII characters we are using are from 32 to 126
    ascii_chars = {}
    for i in range(32, 127):
        char_image = Image.open(f"ASCII-set/{i}.png").convert("L")
        char_image = char_image.resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)
        intensity_vector = np.array(char_image).flatten()
        intensity_vector = intensity_vector / 255.0
        ascii_chars[i] = intensity_vector
    return ascii_chars


# This is the image preprocessing, currently just flattens it a bit 
# (not entirely sure why this has to happen but it works)
def preprocess(image_path): 
    with Image.open(image_path) as img:
        width, height = img.size
        new_height = int(height * 0.4825)
        img_smushed = img.resize((width, new_height), Image.Resampling.LANCZOS)
        return img_smushed


#this method takes all of the pixel_size section of the image and converts them to greyscale intensity vectors
def pixelate_sections(img, pixel_size): 
    img = img.convert("L")
    img_size = img.size
    sections = []

    for i in range(0, img_size[1], pixel_size):
        for j in range(0, img_size[0], pixel_size):
            box = (j, i, j + pixel_size, i + pixel_size)

            section = img.crop(box).resize((pixel_size, pixel_size), resample=Image.Resampling.BILINEAR)
            intensity_vector = np.array(section).flatten()
            intensity_vector = intensity_vector / 255.0
            sections.append(intensity_vector)

    return sections


# this method assigns the sections to ASCII characters, currently just on euclidean distance
def classify_image_sections_combined(img, pixel_size):
    ascii_chars = load_ascii(pixel_size)
    sections = pixelate_sections(img, pixel_size)
    
    ascii_image = []
    weighted_scores = []

    for section in tqdm(sections):
        distances = {}
        for char, vec in ascii_chars.items():
            
            # calculates the euclidean distance
            euclidean_dist = euclidean(section, vec)
            max_euclidean_dist = np.sqrt(len(section))
            normalized_euclidean = euclidean_dist / max_euclidean_dist
            euclidean_accuracy = 1 - normalized_euclidean

            # calculates the cosine similarity
            cosine_sim = cosine_similarity([section], [vec])[0][0]

            weighted_score = (euclidean_weight * euclidean_accuracy) + (cosine_sim_weight * (1 - cosine_sim))
            
            distances[char] = weighted_score

        closest_char = max(distances, key=distances.get)
        ascii_image.append(chr(closest_char))
        weighted_scores.append(max(distances.values())) # adds the score of the chosen character

    # calculates the average of the scores for the chosen characters
    closeness_score = sum(weighted_scores) / len(weighted_scores) 
    
    img = img.convert("L")
    img_size = img.size
    ascii_art = ""

    counter = 0
    for i in range(0, img_size[1], pixel_size):
        row = ""
        for j in range(0, img_size[0], pixel_size):
            row += ascii_image[counter]
            counter += 1
        ascii_art += row + "\n"
    
    return ascii_art, closeness_score


#converts the char array representing the art to a .txt file
def save_ascii_art(ascii_art, output_file):
    with open(output_file, 'w') as f:
        f.write(ascii_art)


# Does everything!
def asciify(image_path, output_file, pixel_size):
    smushed = preprocess(image_path)
    ascii_image, closeness_score = classify_image_sections_combined(smushed, pixel_size)


    # if "output-files/" not in image_path:  
    #     output_file = "output-files/" + image_path.replace(".png", ".txt")
    # else:
    #     output_file = image_path.replace(".png",".txt")
    save_ascii_art(ascii_image, output_file)
    #print(f"ASCII art saved to {output_file}. Closeness Score = {closeness_score}")
    return closeness_score #used for testing, gives an accuracy score for the image


#asciify(image_path=image_path, output_file=output_file, pixel_size=pixel_size)