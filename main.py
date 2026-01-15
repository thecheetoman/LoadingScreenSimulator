import pygame
import sys
import random
import time

pygame.init()

# -----------------------------
# Window Setup
# -----------------------------
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Loading Screen Simulator")

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
TOTAL_SHADERS = 100
current_shader = 0
shader_start_time = pygame.time.get_ticks()
shader_compile_duration = random.randint(0, 100)  # ms for current shader

# -----------------------------
# Loading Bar State
# -----------------------------
progress = 0.0
progress_speed = 0.02  # intentionally slow and inconsistent

messages = [
    "Optimizing coconut physics...",
    "Reticulating splines...",
    "Loading assets that don't exist...",
    "Calibrating loading bar...",
    "Simulating progress...",
    "Pretending to load textures...",
    "Generating meaningless numbers...",
    "Re-evaluating life choices...",
    "Rendering the void...",
    "Almost there (not really)..."
]

current_message = random.choice(messages)
message_timer = 0
message_interval = 2000  # ms

# -----------------------------
# Draw Loading Bar
# -----------------------------
def draw_loading_bar(surface, x, y, w, h, progress):
    pygame.draw.rect(surface, (80, 80, 80), (x, y, w, h), border_radius=6)
    inner_width = int(w * progress)
    pygame.draw.rect(surface, (0, 200, 255), (x, y, inner_width, h), border_radius=6)

# -----------------------------
# Main Loop
# -----------------------------
while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((20, 20, 20))

    # -----------------------------
    # Phase 1: Compiling Shaders
    # -----------------------------
    if phase == PHASE_COMPILING:
        now = pygame.time.get_ticks()
        # Check if current shader "finished compiling"
        if now - shader_start_time >= shader_compile_duration:
            current_shader += 1
            if current_shader >= TOTAL_SHADERS:
                # Move to loading phase
                phase = PHASE_LOADING
            else:
                # Start next shader
                shader_start_time = now
                shader_compile_duration = random.randint(0, 2000)

        # Draw compiling UI
        title = FONT.render("Compiling Shaders...", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        # Progress based on shaders compiled
        shader_progress = current_shader / TOTAL_SHADERS
        draw_loading_bar(screen, 150, 200, 500, 40, shader_progress)

        # Shader count text
        shader_text = SMALL_FONT.render(
            f"Compiling shader {current_shader}/{TOTAL_SHADERS}",
            True,
            (200, 200, 200)
        )
        screen.blit(shader_text, (WIDTH // 2 - shader_text.get_width() // 2, 260))

        # Estimated nonsense time
        est_text = SMALL_FONT.render(
            "Estimated time remaining: unknown",
            True,
            (150, 150, 150)
        )
        screen.blit(est_text, (WIDTH // 2 - est_text.get_width() // 2, 300))

    # -----------------------------
    # Phase 2: Eternal Loading
    # -----------------------------
    elif phase == PHASE_LOADING:
        # Update fake progress (never reaches 100%)
        progress += progress_speed * (random.random() * 0.5)
        if progress > 0.98:
            progress = 0.75  # reset slightly to simulate "almost done"

        # Update loading message
        message_timer += dt
        if message_timer >= message_interval:
            current_message = random.choice(messages)
            message_timer = 0

        title = FONT.render("Loading...", True, (255, 255, 255))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        draw_loading_bar(screen, 150, 200, 500, 40, progress)

        msg = SMALL_FONT.render(current_message, True, (200, 200, 200))
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 260))

        percent = SMALL_FONT.render(f"{int(progress * 100)}%", True, (255, 255, 255))
        screen.blit(percent, (WIDTH // 2 - percent.get_width() // 2, 320))

    pygame.display.flip()