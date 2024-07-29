import asciify
import plotasciify
import os
from tkinter.filedialog import askopenfilename
from tkinter import filedialog
                                   
#        __   _____     _    _   _____  __      __ggg__          
#     _gM""M  ""@PPM"  g@   #@L  @E``Mg $E      @`   `           
#     0&___     #L    _@@L _@NL  @L _@# $L      @_____           
#       `""0g   0L    #E^@_@F @  BMMP`  BL     JN"""``           
#    a_   _@#  _$L__ _@  9N#  0L B      @L  __ Jg                
#     "MMM"`  "P"""" 'F   P   'P "      MNMMP"  MNNNNR           
#                                           
#         _      _____    __ggg ggggg_ ggggg_  g@NNN@ g_    g,   
#       _@@L    @M` ``   g0"  P   @ ``   BL``  @      ^@_  @#    
#      y0`_B    MN@@g_  @F        @      @L    @WNNNK   0yg0     
#     gNMMP@_        0L @         @      BL    @         $N      
#    g#    3g  0g___@#` 3@ggg#^ _w@wgy __@&gg  @        g0`      
#           `    ```            ``     ``      "        `        
# 
# This file is a very simple interface for using ASCIIFY with prompts on the command line.                                   
                                                               

input_file_path = input("Input file name (include .png or .jpg, must be in input-files directory): ")
output_file_name = input("Output file name (will be in output-files directory, don't need to type .txt): ")
pixel_size = input("pixel size: ")

input_file_path = "input-files/" + input_file_path
output_file_name = "output-files/" + output_file_name + ".txt"
asciifier = asciify.Asciify(pixel_size=int(pixel_size))
asciifier.asciify(image_path=input_file_path, output_file=output_file_name)

# asciify_plotter = plotasciify.PlotAsciify(csv_file="output-files/blank.csv",image_path="input-files/blank.jpg",pixel_size_low=1,pixel_size_high=250)
# asciify_plotter.test_data()