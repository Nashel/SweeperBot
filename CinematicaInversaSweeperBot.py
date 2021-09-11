import sim
import numpy as np
import sympy as sp
from sympy import *

from sympy.physics.vector import init_vprinting
init_vprinting(use_latex='mathjax', pretty_print=False)

#######################################################################################
# COMUNICACIÓN CON EL COPPELIA Y CREACIÓN DE LOS OBJETOS
#######################################################################################

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
returnCode,handle=sim.simxGetObjectHandle(clientID,'Dummy',sim.simx_opmode_blocking)
dummy = handle


#ESTA FUNCIÓN HAY QUE COMPLEMENTARLA CON LA SIMULACIÓN EN EL COPPELIA
# Función para abrir o cerrar la pinza remotamente:
'''
def gripper(val):
# función que acciona el efector final remotamente
# val es Int con valor 0 ó 1 para desactivar o activar el actuador final. res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,
    res,retInts,retFloats,retStrings,retBuffer=sim.simxCallScriptFunction(clientID,
    "ROBOTIQ_85", sim.sim_scripttype_childscript,"gripper",[val],[],[],"", sim.simx_opmode_blocking)
    return res
'''

ret,joint1=sim.simxGetObjectHandle(clientID,'joint1',sim.simx_opmode_blocking)
ret,joint2=sim.simxGetObjectHandle(clientID,'joint2',sim.simx_opmode_blocking)
ret,joint3=sim.simxGetObjectHandle(clientID,'joint3',sim.simx_opmode_blocking)

#######################################################################################
# CREACIÓN Y TRANFORMACIÓN DE LA MATRIZ
#######################################################################################

''' gripper(0) ''' #Esto abre la pinza, tenemos que configurarlo en el Coppelia

from sympy.physics.mechanics import dynamicsymbols
theta1, theta2, theta3, d1, d2, d3, theta, alpha, a, d  = dynamicsymbols('theta1 theta2 theta3 d1 d2 d3 theta alpha a d')
theta1, theta2, theta3, d1, d2, d3, theta, alpha, a, d

rot = sp.Matrix([[sp.cos(theta), -sp.sin(theta)*sp.cos(alpha), sp.sin(theta)*sp.sin(alpha)],
                 [sp.sin(theta), sp.cos(theta)*sp.cos(alpha), -sp.cos(theta)*sp.sin(alpha)],
                 [0, sp.sin(alpha), sp.cos(alpha)]])
    
trans = sp.Matrix([a*sp.cos(theta),a*sp.sin(theta),d])

last_row = sp.Matrix([[0, 0, 0, 1]])

m = sp.Matrix.vstack(sp.Matrix.hstack(rot, trans), last_row)

# Transformacion: 1r eje de  '0' a '1'
m01 = m.subs({ theta:theta1, d:d1, a:0 , alpha:90*np.pi/180})

# Resolvemos el problema de Sympy para redondear a 0 asignando directamente el valor
m01[0,1]=0
m01[1,1]=0
m01[2,2]=0  #problema al redondear a 0  http://research.iac.es/sieinvens/python-course/source/sympy.html

# Transformacion: 2º eje de  '1' a '2'
m12  = m.subs({ theta:theta2, d:0,a:d2 ,alpha:0})

# Transformacion: 3r eje de  '2' a '3'
m23 = m.subs({ theta:theta3, d:0, a:d3 ,alpha:0})

# Matriz Resultante sin simplificar
m03 = (m01*m12*m23)

# Matriz Resultante podemos simplificarla más :
mbee= sp.Matrix([[sp.trigsimp(m03[0,0].simplify()), sp.trigsimp(m03[0,1].simplify()), sp.trigsimp(m03[0,2].simplify()),sp.trigsimp(m03[0,3].simplify())],
                 [sp.trigsimp(m03[1,0].simplify()), sp.trigsimp(m03[1,1].simplify()), sp.trigsimp(m03[1,2].simplify()),sp.trigsimp(m03[1,3].simplify())],
                 [m03[2,0].simplify(), m03[2,1].simplify(), m03[2,2].simplify(),m03[2,3].simplify()],
                 [m03[3,0].simplify(), m03[3,1].simplify(), m03[3,2].simplify(),m03[3,3].simplify()]])


#######################################################################################
# ACERCAMIENTO AL OBJETO
#######################################################################################

''' gripper(0) ''' #Esto abre la pinza, tenemos que configurarlo en el Coppelia

# Aplicar las coordenadas que recibirá del reconocimiento por visión de computador
x,y,z=7,-13,15 

#MOVIMIENTO HACIA EL OBJETO EN CUESTIÓN
eq1 = (14 * cos(theta2) + 14 * cos(theta2 + theta3))*cos(theta1) - x
eq2 = (14 * cos(theta2) + 14 * cos(theta2 + theta3))*sin(theta1) - y
eq3 = 3 + 14 * sin(theta2) + 14 * sin (theta2 + theta3) - z

q=nsolve((eq1,eq2,eq3),(theta1,theta2,theta3),(1,1,1))

q[0]=q[0]-round(q[0]/(np.pi*2))*2*np.pi
q[1]=q[1]-round(q[1]/(np.pi*2))*2*np.pi
q[2]=q[2]-round(q[2]/(np.pi*2))*2*np.pi

q[0]=q[0]*180/np.pi
q[1]=q[1]*180/np.pi
q[2]=q[2]*180/np.pi

import time
returnCode = sim.simxSetJointTargetPosition(clientID, joint1, q[0], sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint2, q[1], sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint3, q[2], sim.simx_opmode_oneshot)
print(returnCode)

#######################################################################################
# MOVIMIENTO HACIA EL COMPARTIMENTO (parte 1) con cinemática directa para evitar colisiones
#######################################################################################

''' gripper(1) ''' #Esto cierra la pinza, tenemos que configurarlo en el Coppelia

#INTERCAMBIAMOS EL ORDEN DE MOVIMIENTO DE LOS JOINT PARA EVITAR COLISIÓN
returnCode = sim.simxSetJointTargetPosition(clientID, joint2, 0, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint1, 0, sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint3, 0, sim.simx_opmode_oneshot)
print(returnCode)

#######################################################################################
# MOVIMIENTO HACIA EL COMPARTIMENTO (parte 2) con cinemática inversa habiéndolo posicionado ya bien
#######################################################################################


# Aplicar las coordenadas que recibirá del reconocimiento por visión de computador
x,y,z=-1.96,-1,5 #SON COORDENADAS DE EJEMPLO, QUE COINCIDEN CON LAS DEL COMPARTIMENTO DEL ROBOT EN LA SIMULACIÓN

q=nsolve((eq1,eq2,eq3),(theta1,theta2,theta3),(1,1,1))

q[0]=q[0]-round(q[0]/(np.pi*2))*2*np.pi
q[1]=q[1]-round(q[1]/(np.pi*2))*2*np.pi
q[2]=q[2]-round(q[2]/(np.pi*2))*2*np.pi

q[0]=q[0]*180/np.pi
q[1]=q[1]*180/np.pi
q[2]=q[2]*180/np.pi

import time
returnCode = sim.simxSetJointTargetPosition(clientID, joint1, q[0], sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint2, q[1], sim.simx_opmode_oneshot)
print(returnCode)
time.sleep(3)
returnCode = sim.simxSetJointTargetPosition(clientID, joint3, q[2], sim.simx_opmode_oneshot)
print(returnCode)

''' gripper(0) ''' #Esto abre la pinza, tenemos que configurarlo en el Coppelia
#--------------------------------------------------------------------------------------------