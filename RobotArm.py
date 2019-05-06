import RPi.GPIO as GPIO
import pigpio
import time
import numpy as np
import math as m


'''
       ______
      //beta\\
    a//      \\b
    //        \\
 _alpha        \\
       |        \\
 height|         \\|
 ______|__________|| pen

'''


class RobotArm:
    def __init__(self, a, b, height, alpha_servo, beta_servo, gamma_servo):
        pi = pigpio.pi()
        pi.set_mode(alpha_servo, pigpio.OUTPUT) 
        pi.set_mode(beta_servo, pigpio.OUTPUT) 
        pi.set_mode(gamma_servo, pigpio.OUTPUT)
        
        self.__x = -1
        self.__y = -1
        self.__z = -1
        self.__a = a
        self.__b = b
        self.__height = height
        self.__alpha_servo = alpha_servo
        self.__beta_servo = beta_servo
        self.__gamma_servo = gamma_servo
        self.__alpha = 1500
        self.__beta = 1500
        self.__gamma = 1500
        self.__pi = pi
        self.park()

    def end(self):
        self.off_servos()
        self.__pi.stop()

    def line(self, x0, y0, z0, x1, y1, z1, speed=25, smoothness=50):
        self.move_to(x0,y0,z0, 10, 1)
        speed = speed**(-1)
        
        x_step = (x1 - x0)/smoothness
        y_step = (y1 - y0)/smoothness
        z_step = (z1 - z0)/smoothness
        
        for i in range(1, smoothness+1):
            x = x0 + i*x_step
            y = y0 + i*y_step
            z = z0 + i*z_step
            
            self.move_to(x,y,z,1000,1)
            
            time.sleep(speed)

    def drawX(self, i, j, size = 1.5):
        self.move_to(10, 5, 0)
        time.sleep(0.7)
        if i == 0:
            if j == 2:
                x0 = 9 #1
                z0 = -4
                
                x1 = 11 #2
                z1 = -5.5
                
                x2 = 9 #2.1
                z2 = -6
                
                x3=10.5 #2
                z3=-3.5
                
                self.move_to(x0, 5, z0)
     
                self.line(x0, 1, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x0, 3, z0)
                time.sleep(0.3)
                self.line(x2, 2, z2, x3, 2, z3)
                time.sleep(0.3)
                self.move_to(8, 5, 0)
            elif j == 1:
                x0 = 9.2 #1
                z0 = -1
                
                x1 = 11#2
                z1 = -2
                
                x2 = 9.5 #2.1
                z2 = -3
                
                x3=11 #2
                z3=-0.5
                
                self.move_to(x0, 5, z0)
     
                self.line(x0, 0.5, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x0, 3, z0)
                time.sleep(0.3)
                self.line(x2, 0.5, z2, x3, 1, z3)
                time.sleep(0.3)
                self.move_to(8, 5, 0)
            elif j == 0:
                x0 = 10 #1
                z0 = 2.5
                
                x1 = 11.5 #1
                z1 = 0.5
                
                x2 = 9 #1
                z2 = -0.5
                
                x3=12 #2
                z3=3
                
                self.move_to(x0, 3, z0)
     
                self.line(x0, 1, z0, x1, 1, z1)
                time.sleep(0.3)
                self.move_to(x0, 4, z0)
                time.sleep(0.3)
                self.line(x2, 1, z2, x3, 1, z3)
                time.sleep(0.3)
                self.move_to(8, 5, 0)
            
        elif i == 1:
            if j == 0:
                x0 = 12
                z0 = 3
                x1 = 14
                z1 = 1
                
                x2 = 12
                z2 = 1
                x3 = 14.5
                z3 = 3
        
                self.move_to(x0, 5, z0)
                self.line(x0, 2, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 2, z2, x3, 2, z3)
                time.sleep(0.3)
                self.move_to(12, 5, 0)
            elif j == 1:
                x0 = 11.5
                z0 = -0.5
                x1 = 13.5
                z1 = -2
                
                x2 = 12
                z2 = -2
                x3 = 14
                z3 = 0
        
                self.move_to(x0, 5, z0)
                self.line(x0, 2, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 2, z2, x3, 2, z3)
                time.sleep(0.3)
                self.move_to(12, 5, 0)
            if j == 2:
                x0 = 11
                z0 = -3.5
                x1 = 13
                z1 = -5
                
                x2 = 11
                z2 = -5
                x3 = 13.5
                z3 = -3
        
                self.move_to(x0, 5, z0)
                self.line(x0, 2, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 2, z2, x3, 2, z3)
                time.sleep(0.3)
                self.move_to(12, 5, -3)
            
        elif i == 2:
            if j == 0:   
                x0 = 15
                z0 = 3
                x1 = 16.5
                z1 = 1
                
                x2 = 14.5
                z2 = 1.4
                x3 = 17
                z3 = 3
        
                self.move_to(x0, 5, z0)
                self.line(x0, 2, z0, x1, 2, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 2, z2, x3, 2, z3)
                time.sleep(0.3)
                self.move_to(14, 8, 1)
            elif j == 1:  
                x0 = 14.5
                z0 = 0
                x1 = 16.5
                z1 = -1.5
                
                x2 = 14.5
                z2 = -1
                x3 = 17
                z3 = 0.5
        
                self.move_to(x0, 5, z0)
                self.line(x0, 3, z0, x1, 3, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 3, z2, x3, 3, z3)
                time.sleep(0.3)
                self.move_to(14, 8, -2)
            elif j == 2:  
                x0 = 14
                z0 = -2.5
                x1 = 16
                z1 = -4
                
                x2 = 14.5
                z2 = -4
                x3 = 16.5
                z3 = -2
        
                self.move_to(x0, 5, z0)
                self.line(x0, 3.5, z0, x1, 3.5, z1)
                time.sleep(0.3)
                self.move_to(x1, 6, z1)
                time.sleep(0.3)
                self.move_to(x2, 6, z2)
                self.line(x2, 3.5, z2, x3, 3.5, z3)
                time.sleep(0.3)
                self.move_to(14, 8, -2)
        self.park()
        
    def park(self):
        self.__pi.set_servo_pulsewidth(self.__alpha_servo, 1500)
        self.__pi.set_servo_pulsewidth(self.__beta_servo, 2000)
        self.__pi.set_servo_pulsewidth(self.__gamma_servo, 2500)
        self.__alpha = 1500
        self.__beta = 2000
        self.__gamma = 2500
        time.sleep(1)
        self.off_servos()

    def off_servos(self):
        self.__pi.set_servo_pulsewidth(self.__alpha_servo, 0)
        self.__pi.set_servo_pulsewidth(self.__beta_servo, 0)
        self.__pi.set_servo_pulsewidth(self.__gamma_servo, 0)

    def move_to(self, x, y, z, speed=400, smoothness=100):
        # finding angles
        a = self.__a
        b = self.__b
        c = m.sqrt(x**2 + y**2 + z**2)
        h = self.__height

        alpha = 0
        if -1<= (c**2+x**2-y**2)/(2*c*x) <= 1 and -1 <= (a**2+c**2-b**2)/(2*a*c) <= 1 and -1 <= x/m.sqrt(h**2+x**2) <= 1:
            alpha = m.acos(x/m.sqrt(x**2+y**2)) + m.acos((a**2+c**2-b**2)/(2*a*c)) - m.acos(x/m.sqrt(h**2+x**2))
        

        beta = 0
        if -1<=(a**2 + b**2 - c**2)/(2*a*b) <= 1:
            beta = m.acos((a**2 + b**2 - c**2)/(2*a*b))
        
        gamma = 0
        if -1 <= z/m.sqrt(x**2+z**2) <= 1:
            gamma = m.acos(z/m.sqrt(x**2+z**2))
        self.__x = x
        self.__y = y
        self.__z = z
        
        # rotate
        speed = speed**(-1)
        
        alpha_to = 500+((m.degrees(alpha)/18)*200)
        beta_to = 500+((m.degrees(beta)/18)*200)
        gamma_to = 500+((m.degrees(gamma)/18)*200)
        #print("betato", beta_to)
        
        alpha_step = (alpha_to - self.__alpha)/smoothness
        beta_step = (beta_to - self.__beta)/smoothness
        gamma_step = (gamma_to - self.__gamma)/smoothness
        
        #print(self.__alpha, self.__beta, self.__gamma)
        
        for i in range(1, smoothness+1):
            angle_a = self.__alpha + i*alpha_step
            angle_b = 3000- (self.__beta + i*beta_step)
            angle_g = self.__gamma + i*gamma_step
            #print(round(angle_a,2), round(angle_b,2), round(angle_g,2))
            
            #print(i, round(angle_a, 1), round(angle_b, 1), round(angle_g, 1))
            self.__pi.set_servo_pulsewidth(self.__alpha_servo, round(angle_a,2))
            self.__pi.set_servo_pulsewidth(self.__beta_servo, round(angle_b,2))
            self.__pi.set_servo_pulsewidth(self.__gamma_servo, round(angle_g,2))
            
            time.sleep(speed)

   
        self.__alpha = alpha_to
        self.__beta = beta_to
        self.__gamma = gamma_to

        #print(self.__alpha, self.__beta, self.__gamma, "\n")

    def __str__(self):
        return "({0};{1};{2})".format(self.__x, self.__y, self.__z)


#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(7,GPIO.OUT)
#GPIO.setup(5,GPIO.OUT)
#GPIO.setup(3,GPIO.OUT)

#alpha = GPIO.PWM(7,50)
#beta = GPIO.PWM(5,50)
#gamma = GPIO.PWM(3,50)

#alpha.start(7.5)
#beta.start(2.5)
#gamma.start(7.5)

arm = RobotArm(11.2, 12, 8, 4, 3, 2)
#current = 500
#smoothness = 50
#speed = 50**(-1)
try:
    while True:
        inp = list(map(float, input().split()))
        #inp[0] = 1000+(15-inp[0]-2.5)*100
       # print(inp[0])
        #print("setting to ",pi.set_servo_pulsewidth(3, inp[0]))
        #print("set to ", pi.get_servo_pulsewidth(3))
        
        #step = (inp[0] - current)/smoothness
        
        #print(self.__alpha, self.__beta, self.__gamma)
        
        #for i in range(1, smoothness+1):
        #    angle= current + i*step
        #    pi.set_servo_pulsewidth(3, angle)
        #    time.sleep(speed)
        #current = inp[0]
        #arm.move_to(x=inp[0], y=inp[1], z=inp[2])
        #degree = float(input())
        #beta.ChangeDutyCycle(15-degree)
        #x = input()
        if inp[0] == 1:
            arm.line(inp[1], inp[2], inp[3], inp[4], inp[5], inp[6])
        elif inp[0] == 2:
            arm.drawX(inp[1], inp[2])
        else:
            arm.move_to(inp[1], inp[2], inp[3])
        
        
except KeyboardInterrupt:
        #alpha.stop()
        #beta.stop()
        #gamma.stop()
        arm.end()

        #GPIO.cleanup()
