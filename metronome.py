import pygame.display
import pygame.mixer
import pygame.image
import pygame.font
import pygame.draw
import pygame.time
import time
import sys
import os
import pyperclip

pygame.init()

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Load resources once
click_sound = pygame.mixer.Sound(resource_path('kick.wav'))
click_sound.set_volume(1.0)  # Default volume
intro_image = pygame.image.load(resource_path('intro.png'))
gameIcon = pygame.image.load(resource_path('ico.png'))
pygame.display.set_icon(gameIcon)

# Screen Setup
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Counter Metronome")

# Colors
WHITE = "#ffffff"
BLACK = "#000000"
GREY = "#7a7a7a"
RED = "#8f0101"
GREEN = "#02960c"
BLUE_SLIDER = "#136cb0"

default_values = {
    "background_1": BLACK,
    "background_2": GREY,
    "bar": RED,
    "counter_zone": GREEN,
}
user_values = default_values.copy()

# Constants for frames
FPS = 60
SUPER_COUNTER_START_1, SUPER_COUNTER_END_1 = 21, 28
SUPER_COUNTER_START_2, SUPER_COUNTER_END_2 = 42, 49
MIDPOINTS = {25, 45}

clock = pygame.time.Clock()

# Fade in and out effect
def fade_in_out(image, fade_time=1000, wait_time=1000):
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(WHITE)
    
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(255 - alpha)
        screen.blit(image, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(fade_time // 51)
    
    time.sleep(wait_time / 1000)

    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(image, (0, 0))
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(fade_time // 51)

# Draw the input window
def draw_input_window(color_inputs, input_active, cursor_pos):
    screen.fill(WHITE)
    global font
    font = pygame.font.Font(None, 24)
    instructions = ["Background 1:", "Background 2:", "Bar Color:", "Counter Zone:"]
    for i, text in enumerate(instructions):
        label = font.render(text, True, BLACK)
        screen.blit(label, (50, 50 + i * 30))
        
        color_box = font.render(color_inputs[i], True, BLACK, GREY if input_active[i] else WHITE)
        pygame.draw.rect(screen, GREY, [200, 50 + i * 30, 150, 25], 2 if input_active[i] else 1)
        screen.blit(color_box, (205, 52 + i * 30))

        # Cursor
        if input_active[i]:
            cursor_pos[i] = min(cursor_pos[i], len(color_inputs[i]))  # Ensure the cursor doesn't go out of bounds
            cursor_x = 205 + font.size(color_inputs[i][:cursor_pos[i]])[0]  # Calculate cursor position based on string length
            pygame.draw.line(screen, BLACK, (cursor_x, 52 + i * 30), (cursor_x, 72 + i * 30), 2)  # Draw cursor line


    # Draw Start and Reset buttons
    start_button = font.render("START", True, WHITE, GREEN)
    reset_button = font.render("Reset to Default", True, WHITE, RED)
    screen.blit(start_button, (250, 170))
    screen.blit(reset_button, (50, 170))

# Validate color
def validate_and_set_color(input_value, default_value):
    if pygame.Color(input_value):
        return input_value
    return default_value

# Input color on screen
def input_screen():
    global user_values

    input_active = [False] * 4
    color_inputs = [user_values["background_1"], user_values["background_2"], user_values["bar"], user_values["counter_zone"]]
    cursor_pos = [len(color_inputs[i]) for i in range(4)]
    ctrl_pressed = False

    running = True
    while running:
        draw_input_window(color_inputs, input_active, cursor_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(4):
                    if 200 <= event.pos[0] <= 350 and 50 + i * 30 <= event.pos[1] <= 75 + i * 30:
                        input_active[i] = True
                        clicked_pos = event.pos[0] - 205
                        cursor_pos[i] = min(len(color_inputs[i]), max(0, font.size(color_inputs[i][:clicked_pos])[0]))
                    else:
                        input_active[i] = False

                if 50 <= event.pos[0] <= 200 and 170 <= event.pos[1] <= 200:
                    user_values = default_values.copy()
                    color_inputs = [user_values["background_1"], user_values["background_2"], user_values["bar"], user_values["counter_zone"]]
                    cursor_pos = [len(color_inputs[i]) for i in range(4)]

                if 250 <= event.pos[0] <= 330 and 170 <= event.pos[1] <= 200:
                    user_values['background_1'] = validate_and_set_color(color_inputs[0], default_values['background_1'])
                    user_values['background_2'] = validate_and_set_color(color_inputs[1], default_values['background_2'])
                    user_values['bar'] = validate_and_set_color(color_inputs[2], default_values['bar'])
                    user_values['counter_zone'] = validate_and_set_color(color_inputs[3], default_values['counter_zone'])
                    running = False  # Exit the loop and start metronome

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    ctrl_pressed = True

                for i in range(4):
                    if input_active[i]:
                        if event.key == pygame.K_RETURN:
                            input_active[i] = False
                        elif event.key == pygame.K_BACKSPACE:
                            color_inputs[i] = color_inputs[i][:cursor_pos[i]-1] + color_inputs[i][cursor_pos[i]:]
                            cursor_pos[i] = max(cursor_pos[i] - 1, 0)
                        elif ctrl_pressed and event.key == pygame.K_v:
                            pasted_text = pyperclip.paste()
                            if pasted_text.startswith("#") and len(pasted_text) == 7:
                                color_inputs[i] = color_inputs[i][:cursor_pos[i]] + pasted_text + color_inputs[i][cursor_pos[i]:]
                                cursor_pos[i] += len(pasted_text)  # Move cursor after pasted text
                        elif event.key == pygame.K_LEFT:
                            cursor_pos[i] = max(cursor_pos[i] - 1, 0)  # Move cursor left
                        elif event.key == pygame.K_RIGHT:
                            cursor_pos[i] = min(cursor_pos[i] + 1, len(color_inputs[i]))  # Move cursor right
                        else:
                            color_inputs[i] = color_inputs[i][:cursor_pos[i]] + event.unicode + color_inputs[i][cursor_pos[i]:]
                            cursor_pos[i] += 1

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    ctrl_pressed = False

        pygame.display.flip()

# Metronome function
def metronome():
    global click_sound
    frame = 0
    volume = 1.0 
    click_sound.set_volume(volume)

    running = True
    prev_background = None
    is_dragging_slider = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 50 <= event.pos[0] <= 550 and 150 <= event.pos[1] <= 160:
                    is_dragging_slider = True
                    volume = (event.pos[0] - 50) / 500
                    click_sound.set_volume(volume)
            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging_slider = False
            elif event.type == pygame.MOUSEMOTION and is_dragging_slider:
                if 50 <= event.pos[0] <= 550:
                    volume = (event.pos[0] - 50) / 500
                    click_sound.set_volume(volume)

        background = user_values['background_1'] if not (SUPER_COUNTER_START_1 <= frame <= SUPER_COUNTER_END_1 or SUPER_COUNTER_START_2 <= frame <= SUPER_COUNTER_END_2) else user_values['background_2']
        if prev_background != background:
            screen.fill(background)
            prev_background = background

        # Volume slider
        slider_handle_x = 50 + volume * 500
        pygame.draw.rect(screen, GREY, [50, 150, 500, 10])
        pygame.draw.rect(screen, BLUE_SLIDER, [slider_handle_x - 5, 150, 10, 10])

        pygame.draw.rect(screen, user_values['bar'], [50, 80, 500, 40])
        pygame.draw.rect(screen, user_values['counter_zone'], [50 + (SUPER_COUNTER_START_1 / FPS) * 500, 80, (SUPER_COUNTER_END_1 - SUPER_COUNTER_START_1) / FPS * 500, 40])
        pygame.draw.rect(screen, user_values['counter_zone'], [50 + (SUPER_COUNTER_START_2 / FPS) * 500, 80, (SUPER_COUNTER_END_2 - SUPER_COUNTER_START_2) / FPS * 500, 40])

        pygame.draw.rect(screen, BLACK, [50 + (frame / FPS) * 500, 80, 5, 40])

        # Sound Play Logic
        if frame == 21:
            click_sound.play()
        elif frame == 45:
            click_sound.play()

        pygame.display.flip()
        frame = (frame + 1) % FPS
        clock.tick(FPS)

# Main program flow
fade_in_out(intro_image)
input_screen()
metronome()