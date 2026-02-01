import pygame
import serial
import time

#-----Configurations-----
SERIAL_PORT = '/dev/ttyUSB0'  # Change as needed
#Puede que no se tengan los permisos necesarios en linux para acceder al puerto serial en linux
#usar: sudo usermod -a -G dialout $USER para ubuntu/debian
#usar: sudo usermod -a -G uucp $USER para archlinux/manjaro
BAUD_RATE = 115200

#iniciar pygame
pygame.init()
pygame.joystick.init()
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f'Joystick conectado: {joystick.get_name()}')
except:
    print("No se encontro ningun joystick.")
    exit()


#iniciar comunicacion serial
try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.1)
    time.sleep(2)  # Esperar a que la conexion se establezca
    print(f'Conectado a Arduino en {SERIAL_PORT} a {BAUD_RATE} baudios.')
except:
    print(f'No se pudo conectar al puerto serial {SERIAL_PORT}.')
    exit()


#main loop

try:
    while True:
        pygame.event.pump()

        val_x = joystick.get_axis(0)  # Eje X
        val_y = joystick.get_axis(1)  # Eje Y

        
        enviar_x = int(val_x * 100)
        enviar_y = int(val_y * -100)

        #zona muerta
        if abs(enviar_x) < 10:
            enviar_x = 0
        if abs(enviar_y) < 10:
            enviar_y = 0
        
        #formato de datos
        mensaje = f'{enviar_x},{enviar_y}\n'

        arduino.write(mensaje.encode())

        #DEBUG
        print(f"Enviando -> X: {enviar_x}, Y: {enviar_y}", end="\r")

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nSaliendo...")
    arduino.close()
    pygame.quit()
