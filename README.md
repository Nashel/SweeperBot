## Índice de contenidos
* [¿Qué es SweeperBot?](#SweeperBot)
* [Instalación de dependencias](#instalar)
* [Arquitectura HW](#HW)
* [Diseño de las piezas 3D](#Diseño3D)
* [Simulación](#Funcionamientos)

<a name="SweeperBot"></a>
# SweeperBot

SweeperBot es un robot autónomo diseñado para ayudar en el ámbito medioambiental, y que es el producto final de una idea que garantiza una mayor sostenibilidad del entorno que nos rodea. 
Para llevar a cabo su cometido, el robot se contempla como un vehículo autónomo, de manera que pueda moverse libremente y sin ningún tipo de supervisión para la búsqueda de residuos. Para la recolección de estos, el robot dispone de un brazo mecánico con pinza, esta le permitirá agarrar los desechos y soltarlos en unos compartimentos a modo de reciclaje. 

<a name="instalar"></a>
### Instalación de las dependencias

- Tensorflow(Version: 2.4.1):  pip install tensorflow
- Imageai(Version: 2.1.6): pip install imageai
- Keras(Version: 2.1.6): pip install keras
- opencv2(Version 2.4.9): pip install opencv-python
- numpy(Version: 1.20.3): pip install numpy
- sympy(Version: 4.0.1): pip install simpy
- Yolo.h5 (https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5)

<a name="HW"></a>
### Arquitectura HW
<p align="center">
<img src="images/componentes.PNG" height="300">
  
  **Movimiento del vehículo**
  
Se han conectado los dos motores de las ruedas al controlador L298 junto con la corriente de las 4 pilas de 1,5 Voltios, este controlador actúa de intermediario entre la Raspberry y los movimientos del vehículo. El controlador se ha conectado también a la Raspberry Pi. 

  **Cinemática inversa del brazo**
  
Los 3 motores utilizados para mover el brazo en el plano de 3 ejes, y el servomotor que controla la apertura de la pinza se han conectado a la placa i2c, esta facilita la comunicación entre la raspberry y los componentes. La placa i2c está conectada a 4 pilas de 1,5 Voltios y a la Raspberry Pi. 

  **Reconocimiento de objetos**
  
La cámara es alimentada por dos pilas de 1,5 Voltios y controlada directamente por la Raspberry.

</p>

<a name="Diseño3D"></a>
## Diseño 3D

El proyecto contiene archivos STL para formar la estructura del robot.


### Robot montado
<p align="center">
<img src="images/image13.png" width="300" height="300">

<img src="images/image14.png" width="300" height="300">

<img src="images/image15.png" width="300" height="300">
</p>

### Pinza
<p align="center">
<img src="images/image26.jpg" height="300">
</p>

### Articulaciones del brazo
<p align="center">
<img src="images/image25.png" height="300">
<img src="images/image27.png" height="300">
</p>

### Base del brazo
<p align="center">
<img src="images/image29.png" width="300" height="300">
<img src="images/image30.png" width="300" height="300">
</p>

### Base de la carrocería
<p align="center">
<img src="images/image32.png" height="300">
</p>

### Soporte de la caja
<p align="center">
<img src="images/image34.png" height="300">
</p>
<p align="center">
<img src="images/image35.png" width="300">
</p>
  
### Caja con corpantimentos
<p align="center">
<img src="images/image37.png" width="300" height="300">
</p>
  
## Reconocimiento de objetos
Se ha utilizado el lenguaje Python para realizar el reconocimiento e identificación de formas, y se ha importado la librería “opencv” para obtener imágenes de la cámara. Y la librería “imageai” que utiliza “tensorflow”, una librería orientada a construir y entrenar redes neuronales, para utilizar un modelo de reconocimiento de objetos (Yolo).

<p align="center">
<img src="images/image4.png" height="250">
<img src="images/image5.png" height="250">
</p>

Tras unas adaptaciones se ha utilizado el modelo para reconocer objetos en una simulación en CoppeliaSim.

<p align="center">
<img src="images/image2.png" height="300">
</p>

Los datos de cada objeto se gestionan con Python como una lista de diccionarios.

<p align="center">
<img src="images/image24.png" height="200">
</p>

<a name="Funcionamientos"></a>
## Simulación

Se ha simulado el comportamiento del robot con CoppeliaSim para recrear un espacio con una serie de diferentes objetos, que se interponen en el camino del robot. Éste, pudiendo detectarlos, recogerlos y almacenarlos en los compartimentos correspondientes, simula su correspondiente actuación. 

### Ruedas
Se han utilizado las siguientes ruedas para la simulación.
<p align="center">
<img src="images/image16.png" height="300">
<img src="images/image17.png" height="300">
</p>

### Ruedas incorporadas en el stl de la caja
<p align="center">
<img src="images/image18.png" width="300" height="300">
</p>

### Funcionamiento

El robot gira hasta detectar un objeto que le interesa.

<p align="center">
<img src="images/image8.png" height="300">
</p>

Una vez detectado se acerca a él, lo recoge y lo almacena en el compartimento que le pertoque.

<p align="center">
<img src="images/image19.png" height="300">
<img src="images/image3.png" height="300">
</p>

<p>
  El siguiente enlace contiene el video promocional de SweeperBot (https://youtu.be/OWggp3zetLo)
</p>

