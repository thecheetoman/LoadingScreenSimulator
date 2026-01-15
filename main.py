import pygame
import sys
import random
import time
import os

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path

pygame.init()

# -----------------------------
# Window Setup
# -----------------------------
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen Simulator")
icon = pygame.image.load(resource_path("icon.png"))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 28)
SMALL_FONT = pygame.font.SysFont("consolas", 20)

# -----------------------------
# Phases
# -----------------------------
PHASE_COMPILING = 0
PHASE_LOADING = 1
phase = PHASE_COMPILING

# -----------------------------
# Compiling Shaders State
# -----------------------------
TOTAL_SHADERS = 571
current_shader = 0
shader_start_time = pygame.time.get_ticks()
shader_compile_duration = random.randint(0, 50)  # ms for current shader

#things
progress = 0.0
progress_speed = 0.0001  # intentionally slow and inconsistent

messages = [
    "Initializing...",
    "Loading compiled shaders",
    "Checking for updates",
    "Update found",
    "Downloading update files",
    "Initializing updater...",
    "Installing update",
    "Re-starting back-end",
    "Attempting to start",
    "Failed process, try again"
]

# message system changed to sequential
message_index = 0
current_message = messages[message_index]
message_timer = 0
message_interval = 50000  # ms

#draw bar loading
def draw_loading_bar(surface, x, y, w, h, progress):
    pygame.draw.rect(surface, (80, 80, 80), (x, y, w, h), border_radius=6)
    inner_width = int(w * progress)
    pygame.draw.rect(surface, (0, 200, 255), (x, y, inner_width, h), border_radius=6)

# thing-
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((20, 20, 20))

    #ue5 simulator
    if phase == PHASE_COMPILING:
        now = pygame.time.get_ticks()
        #  current shader "finished compiling"
        if now - shader_start_time >= shader_compile_duration:
            current_shader += 1
            if current_shader >= TOTAL_SHADERS:
                # loading phase
                phase = PHASE_LOADING
            else:
                # next shader
                shader_start_time = now
                shader_compile_duration = random.randint(0, 2000)

        # ui is compiling UI
        title = FONT.render("Compiling Shaders...", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # yes based on shaders compiled
        shader_progress = current_shader / TOTAL_SHADERS
        draw_loading_bar(screen, 150, 200, 500, 40, shader_progress)

        # text is shows count count text
        shader_text = SMALL_FONT.render(
            f"Compiling shader {current_shader}/{TOTAL_SHADERS}",
            True,
            (200, 200, 200)
        )
        screen.blit(shader_text, (WIDTH // 2 - shader_text.get_width() // 2, 260))

        # tuffness nonsense time
        est_text = SMALL_FONT.render(
            "Estimated time remaining: yes",
            True,
            (150, 150, 150)
        )
        screen.blit(est_text, (WIDTH // 2 - est_text.get_width() // 2, 300))

    #other part
    elif phase == PHASE_LOADING:
        # torture
        progress += progress_speed * (random.random() * 0.5)
        if progress > 0.98:
            progress = 0.75  #never finish

        # updat loading message
        message_timer += dt
        if message_timer >= message_interval:
            message_index = (message_index + 1) % len(messages)
            current_message = messages[message_index]
            message_timer = 0

        title = FONT.render("Loading...", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        draw_loading_bar(screen, 150, 200, 500, 40, progress)

        msg = SMALL_FONT.render(current_message, True, (200, 200, 200))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 260))

        percent = SMALL_FONT.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        screen.blit(percent, (WIDTH // 2 - percent.get_width() // 2, 320))

    pygame.display.flip()