# Image2hex

Python script utility to convert images files to hexadecimal format compatible with GxEPD2 library.
This script change/adapt the image file to 1 bit depth image (AKA black and white), deleting alpha layer (if it have) and tranforming to BMP format.
Once the image is on a compatible format, it use an adapted version of the Python script BMP2HEX (https://github.com/ZinggJM/GxEPD2) returning an .h file compatible with GxEPD2 library.

Also you can apply geometrical transformation such as down/upscaling and rotate the image.


## Ussage:

```python
>>> image2hex.py [-wi <bytes>] [-hi <bytes>] [-ai <bytes>] <infile>
```
- @param infile     Image file to convert.
- @param width      Image width to apply, it can be higher or lower than the original. [optional]
- @param height     Image height to apply, it can be higher or lower than the original. [optional]
- @param angle      Image rotation to apply. [optional]

Compatible files: 
- JPEG
- BMP
- PNG

## Dependencies:

- [Pillow library](https://pillow.readthedocs.io/en/stable/index.html)
