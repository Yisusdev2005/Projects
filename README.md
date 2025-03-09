# Simple OCR for manga (Linux)
![Screenshot]("https://github.com/Yisusdev2005/Simple-OCR-for-Manga/blob/cf220102c4ec18850a60f62dfaca3d7eafbb3747/captura.png")

# Description
A simple program for Linux to extract the text of a vignette or text balloon from a manga panel.
Note: The images must already be saved in a folder or copied to clipboard to select them.

# You may ask “What is this?”
This is a simple program that I developed in python as a practice to measure my knowledge.
As I am just starting in this world, it gives me great joy to share this little project to you.
It may be missing a lot of things and features, but this is a start for me.
I hope you like it and that it works for your manga translations :)

# Executable
Executable only for Linux.

# How to use it?
Just unzip the .zip file, go into the dist folder and click on the executable “MangaTextExtractor” and wait for it to start.
Note: You must have Python 3 installed on your computer.

# Dependencies
Xclip: A Linux mechanism for managing files from the clipboard
Tesseract OCR: This is the optical character recognition engine used by the program.

On Linux: 
> sudo apt-get update && sudo apt-get install -y tesseract-ocr xclip libopencv-dev python3-tk

# Python dependencies (install with pip)
> pip install opencv-python-headless pillow numpy pytesseract

# Japanese language for Tesseract
On Linux: 
> sudo apt-get install tesseract-ocr-jpn tesseract-ocr-jpn-vert 

# Support me!
[Paypal](https://paypal.me/YisusM146?country.x=EC&locale.x=es_XC)
