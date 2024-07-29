import os
import cv2
from tqdm import tqdm
import pandas as pd

import asciify
                                  
#  g   g# ##@NN  @#mg_  @N###  _#Mq,         g#MN; ##N@##*qg   @  @N###  @N###  
#  $L  N    @    N   @  B____  N   @         B_       N   q0   N  @____  @____  
#   B @F    @    N   BL BC``` qN   @          "MNg    N   q0   N  @"```  @````  
#   3@0   __@__  N__g#  B____  B_ _0         __ _N    N    N_ _0  @      @      
#    "`   `""""  ""``   """""   """          `"""     "     """   "      "    
# 
#                     __ ___   ___   _____ _    _  
#     y@L   @BMMM  _g#M@PPM@MM"MN@MM @M"""`%g  yN` 
#    @P3B  ^Nggg_ gN^     J@    [N   @NN@p  X@g@`  
#  _@MMM@L _   _BE$&  __  J@    [N   @       J@`   
#  9F   'P MNNNM"  "MMP` MMMMM NMMMP N       N`    
#
# Creates a folder containing each frame of a video file converted to ASCII

video_path = "input-files/input2.mp4"  # Replace with the path to your video file
frames_dir = "output-files/video_frames" # this directory will be created
output_dir = "output-files/ascii_frames_2" # this directory will be created
pixel_size = 100 #this is the pixel size used


def split_video_to_frames(input_video_path, output_dir):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video_path}")
        return

    # Get the total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Read and save frames one by one
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Construct the output file path
        output_file_path = os.path.join(output_dir, f"frame_{frame_number:04d}.png")

        # Save the frame as a PNG file
        cv2.imwrite(output_file_path, frame)

        frame_number += 1

    # Release the video capture object
    cap.release()


# this method takes an input directory of frames to asciify and asciifys them, placing them in a new directory
def frames_to_ascii(frame_directory, output_dir, pixel_size):
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all files in the frame directory
    frame_files = sorted([f for f in os.listdir(frame_directory) if os.path.isfile(os.path.join(frame_directory, f))])

    for frame_file in tqdm(frame_files, desc="Converting frames to ASCII"):
        frame_path = os.path.join(frame_directory, frame_file)
        output_file_path = os.path.join(output_dir, frame_file)
        output_file_path = output_file_path.replace(".png", ".txt")
        # Run asciify on each frame
        asciify.asciify(frame_path, output_file_path, pixel_size)




split_video_to_frames(video_path, frames_dir)

frames_to_ascii(frames_dir, output_dir, pixel_size)