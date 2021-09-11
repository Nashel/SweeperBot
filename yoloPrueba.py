# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:19:58 2021

@author: Jordi Campoy
"""
from imageai import Detection
import cv2

yolo = Detection.ObjectDetection()
yolo.setModelTypeAsYOLOv3()
yolo.setModelPath("yolo.h5")
yolo.loadModel()
'''
cam = cv2.VideoCapture(0) #0=front-cam, 1=back-cam
cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ## read frames
    ret, img = cam.read()
    #img=cv2.imread("WhatsApp.jpeg")

    ## predict yolo
    img, preds = yolo.detectObjectsFromImage(input_image=img,
                      custom_objects=None, input_type="array",
                      output_type="array",
                      minimum_percentage_probability=70,
                      display_percentage_probability=False,
                      display_object_name=True)
    ## display predictions
    cv2.imshow("", img)
    #cv2.imwrite("cosa.jpg", img)
    print(preds)
    #cv2.waitKey(0)
  
    ## press q or Esc to quit    
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
        break


## close camera
cam.release()
cv2.destroyAllWindows()
'''


img=cv2.imread("cosa.jpg")

img, preds = yolo.detectObjectsFromImage(input_image=img,
                  custom_objects=None, input_type="array",
                  output_type="array",
                  minimum_percentage_probability=40,
                  display_percentage_probability=False,
                  display_object_name=True)

cv2.imshow("", img)
print(preds)
cv2.waitKey(0)
  


## close camera
cv2.destroyAllWindows()