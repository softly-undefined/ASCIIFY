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
#
# This code asciifies a range of pixel_size values
# and stores accuracy scores for each pixel size in a csv_file of your choosing


csv_file = "plotdata.csv" #this is the path to the csv file that data will be added to
image_path = "input-files/test.png" #this is the path to the image you want to use
pixel_size_low = 1 #this is the pixel_size that it will start with
pixel_size_high = 250 #this is the pixel_size that it will end with


class PlotAsciify:


    def __init__(self, csv_file="closeness_scores.csv", image_path="test.png",pixel_size_low=10, pixel_size_high=15):
        self.csv_file = csv_file # this file stores the data being calculated
        self.image_path = image_path
        self.pixel_size_low = pixel_size_low
        self.pixel_size_high = pixel_size_high

    def test_data(self):
        #setting up the directory for the output
        base_output_dir = "output-files"
        image_name = self.image_path.replace(".png", "-dir")
        output_dir = os.path.join(base_output_dir, image_name)
        os.makedirs(output_dir, exist_ok=True)


        if os.path.exists(self.csv_file):
            df = pd.read_csv(self.csv_file)
        else:
            pixel_sizes = range(1,301) #can make this bigger if needed
            df = pd.DataFrame(columns=['pixel_size'])
            df['pixel_size'] = pixel_sizes

        # Creates a new column in the dataframe if one for the input file doesn't exist yet
        if self.image_path not in df.columns:
            df[self.image_path] = None

        closeness_scores = []

        for i in tqdm(range(self.pixel_size_low, self.pixel_size_high), desc="Testing pixel_sizes"):
            pixel_size = i
            # below checks if the index being calculated has already been run earlier
            if pixel_size in df['pixel_size'].values and not df.loc[df['pixel_size'] == pixel_size, self.image_path].isna().all():
                continue

            output_file = os.path.join(output_dir, f"output_{pixel_size}.txt")

            asciifier = asciify.Asciify(pixel_size=pixel_size)
            score = asciifier.asciify(image_path=self.image_path, output_file=output_file)

            closeness_scores.append((pixel_size, score))

        #this part updates the column of the image with the new values.
        if self.image_path in df.columns:
            for pixel_size, score in closeness_scores:
                df.loc[df['pixel_size'] == pixel_size, self.image_path] = score


        df.to_csv(self.csv_file, index=False)


    # this method creates a plot of the column representing the image_path image
    def plot_data(self):
        df = pd.read_csv(self.csv_file)

        if self.image_path not in df.columns:
            raise ValueError(f"Column '{self.image_path}' not found in the DataFrame")



        plt.figure(figsize=(10, 6))

        plt.plot(df['pixel_size'], df[self.image_path], marker='o', label=self.image_path)

        plt.title(f'Closeness Scores vs. Pixel Size ({self.image_path})')
        plt.xlabel('Pixel Size')
        plt.ylabel('Closeness Scores')
        plt.legend()

        plt.grid(True)

        plt.show()

#uncomment to run here
#asciify_plotter = PlotAsciify(csv_file=csv_file,image_path=image_path,pixel_size_low=pixel_size_low,pixel_size_high=pixel_size_high)
#asciify_plotter.test_data()
#asciify_plotter.plot_data()

