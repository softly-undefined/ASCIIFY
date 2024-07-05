import os
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt

import asciify

#   ____    _           ___    __                                       
#  J@MMN@g [@L       g@@NNN@g_3NNN@@NN@@K                               
#  3@L  @@L[@L     _@@"    ^@B    @@L                                   
#  @@@@@N" @@L     @@L      @N    [@L                                   
#  @@``    @@      $@_    _@@C    3@E                                   
#  @@      B@@@g@@# M@@@@@@M`     J@E                                   
#   `      `"""``     ````                                                                                               
#             __      _    _                        _                   
#   _@NN@@  _@NN@g _@@NN@ 3@E  0@ @@@@N@L g@NN@g  g@NN@y4@g   @@        
#  @@F  @N @@F     @N`    [@L  @@ @@" ^M #@C  @E @@C     3@g_@@C        
#  3@L__B@ 3@_____ @&_____3@L__@@ @@     0@___@B 0@_____  ^@@@C         
#   "MNMMNF ^MNNM"  MMNMM` "MNMNN #N      "MNMMNF "MNMM^   @@C          
#                                                         @@F           
#                                                         ""            
#                     __ ___   ___   _____ _    _  
#     y@L   @BMMM  _g#M@PPM@MM"MN@MM @M"""`%g  yN` 
#    @P3B  ^Nggg_ gN^     J@    [N   @NN@p  X@g@`  
#  _@MMM@L _   _BE$&  __  J@    [N   @       J@`   
#  9F   'P MNNNM"  "MMP` MMMMM NMMMP N       N`    

csv_file = "closeness_scores.csv" # this file stores the data being calculated
image_path = "eric.png"
pixel_size_low = 50
pixel_size_high = 55

def test_data(image_path, csv_file, pixel_size_low, pixel_size_high):
    #setting up the directory for the output
    base_output_dir = "output-files"
    image_name = image_path.replace(".png", "-dir")
    output_dir = os.path.join(base_output_dir, image_name)
    os.makedirs(output_dir, exist_ok=True)


    if os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
    else:
        pixel_sizes = range(1,301) #can make this bigger if needed
        df = pd.DataFrame(columns=['pixel_size'])
        df['pixel_size'] = pixel_sizes

    # Creates a new column in the dataframe if one for the input file doesn't exist yet
    if image_path not in df.columns:
        df[image_path] = None

    closeness_scores = []

    for i in tqdm(range(pixel_size_low, pixel_size_high), desc="Testing pixel_sizes"):
        pixel_size = i
        # below checks if the index being calculated has already been run earlier
        if pixel_size in df['pixel_size'].values and not df.loc[df['pixel_size'] == pixel_size, image_path].isna().all():
            continue

        output_file = os.path.join(output_dir, f"output_{pixel_size}.txt")

        score = asciify.asciify(("input-files/" + image_path), output_file, pixel_size) #change here
        closeness_scores.append((pixel_size, score))

    #this part updates the column of the image with the new values.
    if image_path in df.columns:
        for pixel_size, score in closeness_scores:
            df.loc[df['pixel_size'] == pixel_size, image_path] = score


    df.to_csv(csv_file, index=False)


# this method creates a plot of the column representing the image_path image
def plot_data(image_path, csv_file):
    df = pd.read_csv(csv_file)

    if image_path not in df.columns:
        raise ValueError(f"Column '{image_path}' not found in the DataFrame")



    plt.figure(figsize=(10, 6))

    plt.plot(df['pixel_size'], df[image_path], marker='o', label=image_path)

    plt.title(f'Closeness Scores vs. Pixel Size ({image_path})')
    plt.xlabel('Pixel Size')
    plt.ylabel('Closeness Scores')
    plt.legend()

    plt.grid(True)

    plt.show()


#this code will run asciify for all pixel_sizes between the parameter boundaries
test_data(image_path, csv_file, pixel_size_low, pixel_size_high)


#this code will create a plot of the selected image's data in the csv
plot_data(image_path, csv_file)