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


# Setup serial
ser = serial.Serial('COM6', 9600)  # Change COM3 to your Arduino port
time.sleep(2)  # Let the serial port initialize

# Music setup
pygame.mixer.init()
pygame.mixer.music.load("8-Bit-Music")  # Replace with your music file path
pygame.mixer.music.play(-1)  # Loop forever

# Game settings
pygame.init()
WIDTH, HEIGHT = 600, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

snake = [(300, 300)]
direction = (20, 0)
food = (100, 100)

def read_joystick():
    global direction
    while True:
        x, y, button = read_joystick_data(ser)
        if x and y:
            if x < 400:
                direction = (-20, 0)
            elif x > 600:
                direction = (20, 0)
            elif y < 400:
                direction = (0, -20)
            elif y > 600:
                direction = (0, 20)
        time.sleep(0.1)

# Start joystick reader in a thread
threading.Thread(target=read_joystick, daemon=True).start()

# Main game loop
running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])
    snake.insert(0, new_head)

    if new_head == food:
        food = (20 * (time.time_ns() % 30), 20 * (time.time_ns() % 30))  # Random
    else:
        snake.pop()

    win.fill((0, 0, 0))
    for segment in snake:
        pygame.draw.rect(win, (0, 255, 0), (*segment, 20, 20))
    pygame.draw.rect(win, (255, 0, 0), (*food, 20, 20))
    pygame.display.update()

pygame.quit()
ser.close()