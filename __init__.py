__author__ = 'ShangJu'

import os
from PIL import Image, ImageDraw
import cv2


counter = 0

def detect_object(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        "/usr/local/Cellar/opencv/2.4.11/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")

    rect = cascade.detectMultiScale(grayscale, scaleFactor=1.2, minNeighbors=2, flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
                                    minSize=(100, 100))
    result = []
    print(rect)
    for (x, y, w, h) in rect:
        result.append((x, y, x+w, y+h))
    return result


def process(infile):
    size = 250, 250
    image = cv2.imread(infile)
    faces = detect_object(image)
    im = Image.open(infile).convert('L')
    if faces:
        f = faces[0]
        a = im.crop(f)
        a.thumbnail(size, Image.ANTIALIAS)
        return a
    return

def saveFile(infile, save_path, prefix):
    file_name = os.path.join(save_path,  prefix + ".png")
    infile.save(file_name)


if __name__ == "__main__":
    counter = 0
    input = raw_input("which folder do you want to input?")
    dir = "./"+input+"/"

    path = os.path.abspath('.')
    save_path = path+"/temp/"
    for file in os.listdir(dir):
        if not file.startswith('.'):
            print(file)
            counter+=1
            a = process(dir+file)
            if a:
                saveFile(a, save_path, input  +" "+ str(counter))