import sim
import cv2
import time
import numpy as np
import sympy as sp
from sympy import *

#--------------------------------------------------------------------------------------------

def connect(port):
# Establece la conexión a COPPELIA
# El port debe coincidir con el puerto de conexión en VREP  -- DALE AL PLAY !!!
# retorna el número de cliente o -1 si no puede establecer conexión
    sim.simxFinish(-1) # just in case, close all opened connections
    clientID=sim.simxStart('127.0.0.1',port,True,True,2000,5) # Conectarse
    if clientID == 0: print("conectado a", port)
    else: print("no se pudo conectar")
    return clientID

# Conectarse al servidor de COPPELIA
# *** _Hay que ejecutarlo cada vez que se reinicia la simulación ***
clientID = connect(19999)

ret,camera=sim.simxGetObjectHandle(clientID,'camera',sim.simx_opmode_oneshot_wait)

errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,camera,0,sim.simx_opmode_streaming)
time.sleep(0.1)
errprCode,resolution,image = sim.simxGetVisionSensorImage(clientID,camera,0,sim.simx_opmode_buffer)

# processing image
frame = []
frame = np.array(image,dtype = np.uint8)
frame.resize([resolution[0],resolution[1],3])
frame = cv2.flip(frame,0)
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
cv2.imwrite("cosa.jpg", frame)
#cv2.imshow("", frame)
cv2.waitKey(0)

#--------------------------------------------------------------------------------------------