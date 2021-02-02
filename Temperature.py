#!/usr/bin/env python3
# class based on code from Freenove Thermometer project
# https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_Code/11.1.1_Thermometer
import RPi.GPIO as GPIO
import math
from ADCDevice import *

class Temperature(object):
    def __init__(self):
        self.adc = ADCDevice() # define an ADCDevice class object

    def setup(self):
        if(self.adc.detectI2C(0x48)): # detect the pcf8591
            self.adc = PCF8591()
            return True
        elif(self.adc.detectI2C(0x4b)): # detect the ads7830
            self.adc = ADS7830()
            return True
        else:
            print("No correct I2C address found, \n"
            "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
            "Program Exit. \n")
            return False
        
    def get_temp_celsius(self):
        return self.get_temp_kelvin() -273.15                  # calculate temperature (Celsius)

    def get_temp_kelvin(self):
        value = self.adc.analogRead(0)              # read ADC value A0 pin
        voltage = value / 255.0 * 3.3          # calculate voltage
        Rt = 10 * voltage / (3.3 - voltage)    # calculate resistance value of thermistor
        return 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) # calculate temperature (Kelvin)

    def destroy(self):
        self.adc.close()
        GPIO.cleanup()
