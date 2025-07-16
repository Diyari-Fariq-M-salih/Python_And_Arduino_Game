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
pygame.mixer.music.load("8-Bit-Music.mp3")  # Replace with your music file path
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
        print(f"Joystick: X={x}, Y={y}")
        if x is not None and y is not None:
         dead_zone = 50  # Adjust as needed
         center_x = 521
         center_y = 513

         dx = x - center_x
         dy = y - center_y

    # Horizontal movement (left/right)
        if abs(dx) > dead_zone and abs(dx) > abs(dy):  # Prioritize horizontal if stronger
            if dx < 0:
              direction = (-20, 0)  # LEFT
            else:
              direction = (20, 0)   # RIGHT

    # Vertical movement (up/down)
        elif abs(dy) > dead_zone:
            if dy < 0:
              direction = (0, -20)  # UP
            else:
              direction = (0, 20)   # DOWN


        time.sleep(0.1)

# Start joystick reader in a thread
threading.Thread(target=read_joystick, daemon=True).start()

# Main game loop
# Main game loop
running = True
while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    head_x, head_y = snake[0]
    dx, dy = direction

    # Wrap-around
    new_head_x = (head_x + dx) % WIDTH
    new_head_y = (head_y + dy) % HEIGHT
    new_head = (new_head_x, new_head_y)

    snake.insert(0, new_head)

    if new_head == food:
        food = (20 * (time.time_ns() % 30), 20 * (time.time_ns() % 30))  # Random-ish
    else:
        snake.pop()

    win.fill((0, 0, 0))
    for segment in snake:
        pygame.draw.rect(win, (0, 255, 0), (*segment, 20, 20))
    pygame.draw.rect(win, (255, 0, 0), (*food, 20, 20))
    pygame.display.update()


pygame.quit()
ser.close()