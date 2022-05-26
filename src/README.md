# Proyecto_2_TSE

## Esta imagen esta pensada para ser usada en una rasperrypi2

### A continuacion se muestran los pasos a seguir para la configuracion de la imagen:

1. Se deben clonar los siguientes repositorios

        git clone git://git.yoctoproject.org/poky -b dunfell
        
  - Y dentro de la carpeta poky

        git clone https://git.openembedded.org/meta-openembedded -b dunfell

        git clone https://github.com/agherzan/meta-raspberrypi.git -b dunfell

        git clone https://github.com/NobuoTsukamoto/meta-tensorflow-lite -b dunfell
 
 2. Se debe agregar a la carpeta poky la carpeta **meta-archivos**, esta carpeta contiene las recetas y programas necesarios para realizar la deteccion de emociones

#### Al final esta carpeta debe quedar similar a la siguiente imagen:
![pokytree](https://user-images.githubusercontent.com/79667174/168238445-387d6961-e733-4d79-9361-8ac46b552fb9.png)

3. En la carpeta poky entramos al ambiente de trabajo

        source oe-init-build-env

4. Cuando se realiza este proceso, se crea una carpeta llamada **build** dentro de esta se debe reemplazar o modificar la carpeta llamada **conf**, en este paso hay que verificar que:
    - En el archivo **bblayers.conf** la ubicacion exacta de los layers a utilizar
    - En el archivo **local.conf**, la cantidad de nucleos que puede usar su computadora y el tipo de maquina que es este caso es **raspberrypi2**

5. Una vez realizado esto se debe proceder a crear la imagen SATO, para el uso de la USB y una interfaz grafica más comoda, cabe recordar que este proceso es lento y depende mucho de las caracteristicas del computador y del internet. Para esto se entra de nuevo al ambiente de trabajo como en el paso 2 y se seleciona el siguiente comando:

        bitbake core-image-sato

     5.1. Por seguridad antes de proceder con el paso 6, es necesario cocinar la receta y luego volver a cocinar la imagen SATO de esta manera:

        bitbake example
        bitbake core-image-sato
        
6. Cuando termine este proceso se creará un archivo en la ruta **/poky/build/tmp/deploy/images**, el archivo es elgo similar a **core-image-sato-raspberrypi2-20220513074004.rootfs.rpi-sdimg**, este archivo hay que quemarlo en una tarjeta SD, para esto se puede utilizar la herramienta **Disk Image Writer** que pfrece Ubuntu.
  - Solo se debe abrir el archivo con esta herramienta y seleccionar la tarjeta SD con esto comezará el proceso, debe salir algo similar a esto:


 ![SD](https://user-images.githubusercontent.com/79667174/168247280-7c96d4cf-a609-46a0-b99e-751289055b54.png)
 
7. Realizado este proceso, se debe conectar la raspberrypi, con la respectiva SD, el cable HDMI hacia una pantalla asi como un teclado y la alimentación.

8. Cuando haya iniciado se debe ir al siguiente directorio:

        $ cd // 
        $ cd usr/bin/DETECCION 
        
- y Ejecutar el siguiente comando:

        python3 Deteccion_de_emociones.py

#### Hasta aqui la aplicaion esta corriedo de manera local, para hacerlo de manera remota se deben seguir los siguientes pasos:

9. Conectar el cable ethernet a la rasperrypi y conectar la computadora a la misma red

10. Revisar la ip de la raspberypi con el siguiente comando:

        ifconfig eth0
        
11. Una vez que se sabe la ip se debe habilitar la comunicación **ssh** en la computadora y verificar que este activo mediante los siguientes comandos:

        sudo systemctl enable --now ssh
        systemctl status ssh
        
12. Una vez habilitado se procede a realizar la comuniacion con la rasperrypi mediante el siguiente comando:

        ssh root@<dirección_ip_raspberry> -X
        
13. la contraseña para esta configuración es **rsp**

15. En caso de existir un error en la comunicacion de que La identificación del host remoto ha cambiado, se puede utilizar el siguiente comando para arreglarlo:

        ssh-keygen -R <dirección_ip_raspberry>

14 Ya una vez que se logra entrar se puede retomar desde el paso 8 y asi correr el programa remotamente
