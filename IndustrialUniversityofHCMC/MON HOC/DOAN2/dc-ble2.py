import bluetooth
import RPi.GPIO as GPIO
from time import sleep

in1 = 24
in2 = 23
en = 25

in3 = 16
in4 = 20
en2 = 21

temp1 = 1
temp2 = 1

# Khai bao servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)


# Khai bao 2 banh xe phai in1, in2 OUTput 
#GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
# Khai bao 2 banh xe trai in1, in2 OUTput 
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)

# cho phep chan cap xung 2 banh xe phai trai 
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

# 4 banh dung
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)

GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

# Chan cho phep xuat xung tan so 1kHz
p=GPIO.PWM(en,1000)
p.start(25)

p1=GPIO.PWM(en2,1000)
p1.start(25)

host = ""
port = 1        # Raspberry Pi uses port 1 for Bluetooth Communication
# Creaitng Socket Bluetooth RFCOMM communication
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)




print('Bluetooth Socket Created')

try:
        server.bind((host, port))
        print("Bluetooth Binding Completed")
except:
        print("Bluetooth Binding Failed")
server.listen(1) # One connection at a time
# Server accepts the clients request and assigns a mac address.
client, address = server.accept()
print("Connected To", address)
print("Client:", client)


def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	
	'''GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)'''


def main():
 # khai bao bien global
 global temp2
 global temp1
 global send_data
 while(1):

     x = client.recv(1024) 

     if x=='r':
         print("run")
         if(temp1==1):
          GPIO.output(in1,GPIO.HIGH)
          GPIO.output(in2,GPIO.LOW)
          GPIO.output(in3,GPIO.HIGH)
          GPIO.output(in4,GPIO.LOW)
          print("forward")
          #x='z'
         else:
          GPIO.output(in1,GPIO.LOW)
          GPIO.output(in2,GPIO.HIGH)
          GPIO.output(in3,GPIO.LOW)
          GPIO.output(in4,GPIO.HIGH)
          print("backward")
          #x='z'


     elif x=='s':
         print("stop")
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.LOW)
         #x='z'

     elif x=='f':
         print("forward")
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         GPIO.output(in3,GPIO.HIGH)
         GPIO.output(in4,GPIO.LOW)
         temp1=1
         #x='z'

     elif x=='b':
         print("backward")
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         GPIO.output(in3,GPIO.LOW)
         GPIO.output(in4,GPIO.HIGH)
         temp1=0
         #x='z'

     elif x=='1':
         print("low")
         p.ChangeDutyCycle(25)
         p1.ChangeDutyCycle(25)
         #x='z'

     elif x=='2':
         print("medium")
         p.ChangeDutyCycle(50)
         p1.ChangeDutyCycle(50)
         x='z'

     elif x=='3':
         print("high")
         p.ChangeDutyCycle(75)
         p1.ChangeDutyCycle(75)
         #x='z'

    
     elif x=='e':
         GPIO.cleanup()
         break
    
     else:
         print("<<<  wrong data  >>>")
         print("please enter the defined data to continue.....")

     if x=='lef':
         print("re trai")
         SetAngle(10)
         sleep(1)
         SetAngle(45)
        
     elif x=='ri':
         print("re phai")
         SetAngle(60)
         sleep(1)
         SetAngle(45)
    
     elif x=='t':
         print("thang")
         SetAngle(45)
     #client.send(send_data)
     
if __name__=="__main__":
	main()








