import serial
import pygame
import time
import threading

def read_joystick_data(ser):
    try:
        line = ser.readline().decode().strip()
        x, y, button = map(int, line.split(","))
        return x, y, button
    except:
        return None, None, None


