#!/usr/bin/env python

import sys, array, os, textwrap, math, random, argparse
from PIL import Image

def main():
    file_dir = ""
    file_name = ""
    temp_file_name = ""

    parser = argparse.ArgumentParser()
    parser.add_argument ("infile", help="The image file to convert", type=argparse.FileType('r'), nargs='*', default=['-'])
    args = parser.parse_args()
    infile = args.infile

    #Get File path and name
    for f in args.infile:
        if f == '-':
            sys.exit("Error: No file attached")
        file_dir = f.name
    file_name = os.path.splitext(file_dir)[0]
    temp_file_name = file_name + ".bmp"

    #Image transformation to 1 bit BMP image
    _Image = Image.open(file_dir)
    blackAndWhiteImage = _Image.convert("1")
    blackAndWhiteImage.save(temp_file_name)
    _Image.close()

    #Transform into HEX file
    bmp2hex(temp_file_name, _Image.height, _Image.width)

    #Delete temporary file
    os.remove(temp_file_name)

def bmp2hex(file_name, image_height, image_width):

# Only run if launched from commandline
if __name__ == '__main__': main()