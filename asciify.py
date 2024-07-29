from skimage.metrics import structural_similarity as ssim
from scipy.spatial.distance import euclidean
import numpy as np
from PIL import Image
from tqdm import tqdm
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
import os
import pandas as pd

# WELCOME TO                                                                     
#        __        ___       _____ _______ _______  __________      __  
#       g@@_    _@@NNNNK   _@@MM@@^MM@@NNNFMMN@@NNP @N""""M"^@@_   @@F  
#     _@@N@E   q@B____    @@P`   `   B@      [@E    @R_____   0@_ @@F   
#    _@@__@@    "MMNNN@g @@F         @@      [@E    @@MMMMP    %@@@F    
#   g@BMMMN@L ___    _@@L0@_   _g,   @@      [@E    @0          @@F     
#   @0     0@ ^@@@g@@@NM  M@@@@NM` @@@@@@@ g@@@@@@L @0         @@F      
#           `    ````              ``       `       ``         ``       
# by eric bennett
#
# This class is used by all the other files (plotasciify, video, simpleasciify)
# Actionable code shouldn't be written here! For a simple example of using this code
# run the simpleasciify.py file.

class Asciify:
    def __init__(self, pixel_size=100, euclidean_weight=1, cosine_sim_weight=0,image_path="input-files/test.png", output_file="output-files/output_ascii_art.txt"):
        self.pixel_size = pixel_size #the larger this number is, the less characters in the image
        self.euclidean_weight = euclidean_weight # Weights- these should add up to 1
        self.cosine_sim_weight = cosine_sim_weight # right now I'm only using euclidean distance because using cosine similarity gives similar output to 0 and 255 values
        self.image_path = image_path
        self.output_file = output_file


    #loads intensity vectors of pixel_size pixelations of the ascii characters
    def load_ascii(self):
        # ASCII characters we are using are from 32 to 126
        ascii_chars = {}
        for i in range(32, 127):
            char_image = Image.open(f"ASCII-set/{i}.png").convert("L")
            char_image = char_image.resize((self.pixel_size, self.pixel_size), resample=Image.Resampling.BILINEAR)
            intensity_vector = np.array(char_image).flatten()
            intensity_vector = intensity_vector / 255.0
            ascii_chars[i] = intensity_vector
        return ascii_chars


    # This is the image preprocessing, currently just flattens it a bit 
    # (not entirely sure why this has to happen but it works)
    def preprocess(self, image_path): 
        with Image.open(image_path) as img:
            width, height = img.size
            new_height = int(height * 0.4825)
            img_smushed = img.resize((width, new_height), Image.Resampling.LANCZOS)
            return img_smushed


    #this method takes all of the pixel_size section of the image and converts them to greyscale intensity vectors
    def pixelate_sections(self, img): 
        img = img.convert("L")
        img_size = img.size
        sections = []

        for i in range(0, img_size[1], self.pixel_size):
            for j in range(0, img_size[0], self.pixel_size):
                box = (j, i, j + self.pixel_size, i + self.pixel_size)

                section = img.crop(box).resize((self.pixel_size, self.pixel_size), resample=Image.Resampling.BILINEAR)
                intensity_vector = np.array(section).flatten()
                intensity_vector = intensity_vector / 255.0
                sections.append(intensity_vector)

        return sections


    # this method assigns the sections to ASCII characters, currently just on euclidean distance
    def classify_image_sections_combined(self, img):
        ascii_chars = self.load_ascii()
        sections = self.pixelate_sections(img)
        
        ascii_image = []
        weighted_scores = []

        for section in tqdm(sections, desc="Classifying Sections"):
            distances = {}
            for char, vec in ascii_chars.items():
                
                # calculates the euclidean distance
                euclidean_dist = euclidean(section, vec)
                max_euclidean_dist = np.sqrt(len(section))
                normalized_euclidean = euclidean_dist / max_euclidean_dist
                euclidean_accuracy = 1 - normalized_euclidean

                # calculates the cosine similarity
                cosine_sim = cosine_similarity([section], [vec])[0][0]

                weighted_score = (self.euclidean_weight * euclidean_accuracy) + (self.cosine_sim_weight * (1 - cosine_sim))
                
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
        for i in range(0, img_size[1], self.pixel_size):
            row = ""
            for j in range(0, img_size[0], self.pixel_size):
                row += ascii_image[counter]
                counter += 1
            ascii_art += row + "\n"
        
        return ascii_art, closeness_score


    #converts the char array representing the art to a .txt file
    def save_ascii_art(self, ascii_art, output_file):
        with open(output_file, 'w') as f:
            f.write(ascii_art)


    # Does everything!
    def asciify(self, image_path, output_file):
        smushed = self.preprocess(image_path)
        ascii_image, closeness_score = self.classify_image_sections_combined(smushed)
        self.save_ascii_art(ascii_image, output_file)
        #print(f"ASCII art saved to {output_file}. Closeness Score = {closeness_score}")
        return closeness_score #used for testing, gives an accuracy score for the image


    #asciify(image_path=image_path, output_file=output_file, pixel_size=pixel_size)

