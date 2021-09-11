# -*- coding: utf-8 -*-
"""
Created on Mon May 17 14:23:22 2021

@author: nashel
"""

from imageai import Detection
import sim
import cv2
import time
import numpy as np
import sympy as sp
import statistics
from sympy import *

def connect(port):
# Establece la conexión a COPPELIA
# El port debe coincidir con el puerto de conexión en VREP  -- DALE AL PLAY !!!
# retorna el número de cliente o -1 si no puede establecer conexión
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID


yolo = Detection.ObjectDetection()
yolo.setModelTypeAsYOLOv3()
yolo.setModelPath("yolo.h5")
yolo.loadModel()

# Conectarse al servidor de COPPELIA
# *** _Hay que ejecutarlo cada vez que se reinicia la simulación ***
clientID = connect(19999)
ret,camera=sim.simxGetObjectHandle(clientID,'camera',sim.simx_opmode_oneshot_wait)

#ruedas
retCode,jointA=sim.simxGetObjectHandle(clientID,'OmniWheel45_typeA',sim.simx_opmode_blocking)
retCode,jointB=sim.simxGetObjectHandle(clientID,'OmniWheel45_typeB',sim.simx_opmode_blocking)

going4Object = False

while True:

    errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,camera,0,sim.simx_opmode_streaming)
    time.sleep(0.2)
    errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,camera,0,sim.simx_opmode_buffer)
    
    # processing image
    frame = []
    frame = np.array(image,dtype = np.uint8)
    frame.resize([resolution[1],resolution[0],3])
    frame = cv2.flip(frame,0)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    

    ## predict yolo
    img, preds = yolo.detectObjectsFromImage(input_image=frame,
                      custom_objects=None, input_type="array",
                      output_type="array",
                      minimum_percentage_probability=35,
                      display_percentage_probability=False,
                      display_object_name=True)
    
    ## display predictions
    cv2.imshow("", img)
    print(preds)
    if not going4Object:
       retCode = sim.simxSetJointTargetVelocity(clientID, jointA, -0.1,sim.simx_opmode_blocking)
       retCode = sim.simxSetJointTargetVelocity(clientID, jointB, 0.1,sim.simx_opmode_blocking)
    for i in preds:
        if i["name"] == "bottle":
            retCode = sim.simxSetJointTargetVelocity(clientID, jointA, 0,sim.simx_opmode_blocking)
            retCode = sim.simxSetJointTargetVelocity(clientID, jointB, 0,sim.simx_opmode_blocking)
            if statistics.mean([i["box_points"][0],i["box_points"][2]])<400:
                retCode = sim.simxSetJointTargetVelocity(clientID, jointA, 0.02,sim.simx_opmode_blocking)
                retCode = sim.simxSetJointTargetVelocity(clientID, jointB, -0.02,sim.simx_opmode_blocking)
                print("gira izquierda")
            elif statistics.mean([i["box_points"][0],i["box_points"][2]])>600:
                retCode = sim.simxSetJointTargetVelocity(clientID, jointA, -0.02,sim.simx_opmode_blocking)
                retCode = sim.simxSetJointTargetVelocity(clientID, jointB, 0.02,sim.simx_opmode_blocking)
                print("gira derecha")
            going4Object = True
    
    
  
    ## press q or Esc to quit    
    if (cv2.waitKey(1) & 0xFF == ord("q")) or (cv2.waitKey(1)==27):
        break


## close camera
cv2.destroyAllWindows()
