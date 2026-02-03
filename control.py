import pygame
import serial
import time

#-----Configurations-----
SERIAL_PORT = 'COM6'  # Change as needed
#Puede que no se tengan los permisos necesarios en linux para acceder al puerto serial en linux
#usar: sudo usermod -a -G dialout $USER para ubuntu/debian
#usar: sudo usermod -a -G uucp $USER para archlinux/manjaro
BAUD_RATE = 115200
NUM_ROBOTS = 2 # Numero de robots a controlar modificar si se agragan mas robots
#--------------------------------

#iniciar pygame
pygame.init()
pygame.joystick.init()

num_mandos = pygame.joystick.get_count()
if num_mandos == 0:
    print("No se encontro ningun joystick.")
    exit()
print(f"Numero de joysticks conectados: {num_mandos}")

mandos = []
for i in range(num_mandos):
    j = pygame.joystick.Joystick(i)
    j.init()
    mandos.append(j)
    print(f"control {i}: {j.get_name()} -> Asignado a robot {i+1}")
    


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

        for i, joystick in enumerate(mandos):
            robot_id = i + 1

            eje_x = joystick.get_axis(0)  # Eje X
            eje_y = joystick.get_axis(1)  # Eje Y

            val_x = int(eje_x * 100)
            val_y = int(eje_y * -100)

            if abs(val_x) < 10: val_x = 0
            if abs(val_y) < 10: val_y = 0

            mensaje = f"{robot_id},{val_x},{val_y}\n"
            arduino.write(mensaje.encode())
        info = ""

        for i,j in enumerate(mandos):
            axis_x = int(j.get_axis(0)*100)
            info += f"| R{i+1}: {axis_x} "
        print(f"Estado: {info}", end='\r')

        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nSaliendo...")
    arduino.close()
    pygame.quit()
