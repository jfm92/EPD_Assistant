#!/usr/bin/env python


import sys, array, os, textwrap, math, random, argparse
from PIL import Image

def main():
    file_dir = ""
    file_name = ""
    temp_file_name = ""

    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="Image file to convert to 1 bit depth bmp", type=argparse.FileType('r'), nargs='*', default=['-'])
    parser.add_argument("-iw", "--width", help="Change width of the image in pixels", type=int)
    parser.add_argument("-ih", "--height", help="Change height of the image in pixels", type=int)
    parser.add_argument("-ia", "--angle", help="Change the angle of the image in dgrees", type=int)
    args = parser.parse_args()
    infile = args.infile

    # Get File path and name
    for f in args.infile:
        if f == '-':
            sys.exit("Error: No file attached")
        file_dir = f.name
    file_name = os.path.splitext(file_dir)[0]
    
    _Image = Image.open(file_dir)

    # Apply (if any) geometrical transformations to the image
    _Image = img_transform(_Image,args.width,args.height, args.angle)

    # Apply the required transformation to get an 1 bit depth Windows BMP file
    temp_file_name = img2bmp(_Image, file_name)

    #Transform into HEX file
    bmp2hex(temp_file_name, _Image.height, _Image.width)

    #Delete temporary file
    os.remove(temp_file_name)

# Function to transform the image to the required size and rotation
def img_transform(_Image, width, height, angle):
    new_width = _Image.width
    new_height = _Image.height
    new_angle = 0

    if width:
        new_width = width
    if height:
        new_height = height
    if angle:
        new_angle = angle

    size = (new_height, new_width)
    _Image = _Image.resize(size, Image.BICUBIC, box=None, reducing_gap=None)
    _Image = _Image.rotate(new_angle)

    return _Image


# Function to apply format transformation to obtain a 1 bit depth bmp file
def img2bmp(_Image, file_name):
    temp_file_name = file_name + "_tmp" + ".bmp"

    if _Image.mode == "RGBA":
        # If we have alpha channel we need to delete it
        _Image.load()
        _Image_aux = Image.new("RGB", _Image.size, (255, 255, 255))
        _Image_aux.paste(_Image, mask=_Image.split()[3])
        _Image = _Image_aux

    if _Image.mode != "P":
        # Transform to 8 bit depth image -> It's necessary this middle step?
        _Image = _Image.convert("P")

    # Change to 1 bit color depth
    _Image = _Image.convert("1")
    _Image.save(temp_file_name)
    _Image.close()

    return temp_file_name

# Function to transform BMP 1 bit images to hexadcimal compatible with GxEPD2 lib
def bmp2hex(file_dir, image_height, image_width):
    table_width = 16 * 6 # 16 columns in hex
    size_bytes = 1
    file_buffer = ""
    file_buffer_aux = ""
    file_name = os.path.splitext(file_dir)[0]

    fd_img = open(os.path.expanduser(file_dir), "rb")

    #Copy values from file
    image_size = os.path.getsize(os.path.expanduser(file_dir))
    image_array = array.array('B')
    image_array.fromfile(fd_img, image_size)
    fd_img.close()


    # Calculate line width in bytes (Bit depth is 1) and padded byte width
    byte_width   = int(math.ceil(float(image_width)/8.0))
    padded_width = int(math.ceil(float(byte_width)/4.0)*4.0)
    data_offset	 = getLONG(image_array, 10) #?d

    # Calculate size_bytes
    if (image_height > 255) or (image_width >255):
        size_bytes = 2

    # Generate file base on the conversion of bitmap to hex
    file_buffer_aux += "#include <pgmspace.h>\n\n"
    file_buffer_aux += "uint8_t " + file_name + "_height = " + str(image_height) + ";\n"
    file_buffer_aux += "uint8_t " + file_name + "_width = " + str(image_width) + ";\n\n"
    file_buffer_aux += "const unsigned char " + file_name + "[] PROGMEM = {\n"

    for i in range(image_height):
        for j in range (byte_width):
            pix_pos = data_offset + ((image_height-1-i) * padded_width) + j
            pix_value = image_array[pix_pos] ^ 0xFF 
            file_buffer += "{0:#04x}".format(pix_value) + ", "
    
    file_buffer = textwrap.fill(file_buffer[:-2], table_width)

    fd_hex = open(file_name + ".h","w")
    fd_hex.write(file_buffer_aux + file_buffer + "};")

    fd_hex.close()
    fd_img.close()

# Utility function. Return a long int from array (little endian)
def getLONG(a, n):
	return (a[n+3] * (2**24)) + (a[n+2] * (2**16)) + (a[n+1] * (2**8)) + (a[n])

# Only run if launched from commandline
if __name__ == '__main__': main()