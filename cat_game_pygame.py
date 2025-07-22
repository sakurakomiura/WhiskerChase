import pygame
import random
import sys

# Initialization
pygame.init()

# Game start flag
game_started = False

# Game reset function
def reset_game():
    global cat_x, cat_y, mouse_x, mouse_y, game_over
    cat_x, cat_y = WIDTH // 2, HEIGHT // 2
    mouse_x = random.randint(0, WIDTH - MOUSE_SIZE)
    mouse_y = random.randint(0, HEIGHT - MOUSE_SIZE)
    game_over = False

# Screen size
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whisker Chase 🐱🐭")

# Load background image
background_img = pygame.image.load(r"C:\Users\sakuc\My Project\Whisker Chase\background.png").convert_alpha()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Cat and mouse sizes
CAT_SIZE = 70
MOUSE_SIZE = 50

# Movement speed
CAT_SPEED = 15     # Slower for the cat
MOUSE_SPEED = 100 # Faster for the mouse

# Load images for cat and mouse
cat_img = pygame.image.load(r"C:\Users\sakuc\My Project\Whisker Chase\cat.png").convert_alpha()
mouse_img = pygame.image.load(r"C:\Users\sakuc\My Project\Whisker Chase\mouse.png").convert_alpha()


# Resize images to match character sizes
cat_img = pygame.transform.scale(cat_img, (CAT_SIZE, CAT_SIZE))
mouse_img = pygame.transform.scale(mouse_img, (MOUSE_SIZE, MOUSE_SIZE))

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
GRAY = (180, 180, 180)
RED = (255, 0, 0)


# Initial positions
cat_x, cat_y = WIDTH // 2, HEIGHT // 2
mouse_x = random.randint(0, WIDTH - MOUSE_SIZE)
mouse_y = random.randint(0, HEIGHT - MOUSE_SIZE)

# Fonts
TEXT_COLOR = (100, 70, 50)
font = pygame.font.SysFont("Comic Sans MS", 36)
small_font = pygame.font.SysFont("Comic Sans MS", 24)

# Game loop setup
clock = pygame.time.Clock()
game_over = False
elapsed_time = 0

while True:
    # Draw the background
    screen.blit(background_img, (0, 0))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Exit the game
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # Start the game when SPACE is pressed
            if not game_started and event.key == pygame.K_SPACE:
                    game_started = True
                    game_over = False
                    # Reset cat and mouse positions
                    cat_x, cat_y = WIDTH // 2, HEIGHT // 2
                    mouse_x = random.randint(0, WIDTH - MOUSE_SIZE)
                    mouse_y = random.randint(0, HEIGHT - MOUSE_SIZE)
                    # Record the start time
                    start_ticks = pygame.time.get_ticks()

            # Restart the game after game over when SPACE is pressed
            elif game_over and event.key == pygame.K_SPACE:
                game_started = True
                game_over = False
                # Reset positions
                cat_x, cat_y = WIDTH // 2, HEIGHT // 2
                mouse_x = random.randint(0, WIDTH - MOUSE_SIZE)
                mouse_y = random.randint(0, HEIGHT - MOUSE_SIZE)
                # Record the new start time
                start_ticks = pygame.time.get_ticks()

    if not game_started:
        # Title screen
        title_font = pygame.font.SysFont("Kristen ITC", 52)
        info_font = pygame.font.SysFont("Comic Sans MS", 24)

        # Draw the background
        screen.blit(background_img, (0, 0))

        # Draw characters first
        screen.blit(cat_img, (cat_x, cat_y))
        screen.blit(mouse_img, (mouse_x, mouse_y))

        # Draw text last
        title_text = title_font.render("Whisker Chase", True, (80, 50, 20))
        start_text = info_font.render("Press SPACE to start", True, (100, 80, 60))

        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))

        # Render the instruction text (without centering it first)
        control_text = info_font.render("Use W A S D to move the cat!", True, (100, 80, 60))

        # Get the total width: text + image + margin
        cat_icon = pygame.transform.scale(cat_img, (30, 30))
        total_width = control_text.get_width() + cat_icon.get_width() + 5  # 5px margin

        # Calculate X position to center the whole combo
        start_x = WIDTH // 2 - total_width // 2
        y_pos = HEIGHT // 2 + 80

        # Draw the text
        screen.blit(control_text, (start_x, y_pos))

        # Draw the image right after the text
        screen.blit(cat_icon, (start_x + control_text.get_width() + 5, y_pos))

    else:    
        # Cat movement (keyboard input)
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_w]:
                cat_y -= CAT_SPEED
            if keys[pygame.K_s]:
                cat_y += CAT_SPEED
            if keys[pygame.K_a]:
                cat_x -= CAT_SPEED
            if keys[pygame.K_d]:
                cat_x += CAT_SPEED

            # Keep cat within screen bounds
            cat_x = max(0, min(WIDTH - CAT_SIZE, cat_x))
            cat_y = max(0, min(HEIGHT - CAT_SIZE, cat_y))

            # Mouse movement (prediction + wall avoidance)）
            dx = mouse_x - cat_x
            dy = mouse_y - cat_y
            distance = (dx**2 + dy**2)**0.5

            # Cat's movement direction (difference from previous position)）
            if 'prev_cat_x' not in globals():
                prev_cat_x, prev_cat_y = cat_x, cat_y

            cat_dx = cat_x - prev_cat_x
            cat_dy = cat_y - prev_cat_y

            # Evasion behavior when cat is close
            if distance < 200:
                # Escape vector predicting cat's movement direction
                avoid_dx = dx + (-cat_dx * 5)
                avoid_dy = dy + (-cat_dy * 5)

                # Wall avoidance adjustment (guide away from edges)
                if mouse_x < 60:  # Near left edge
                    avoid_dx += 100
                elif mouse_x > WIDTH - MOUSE_SIZE - 60:  # Near right edge
                    avoid_dx -= 100
                if mouse_y < 60:  # Near top edge
                    avoid_dy += 100
                elif mouse_y > HEIGHT - MOUSE_SIZE - 60:  # Near bottom edge
                    avoid_dy -= 100

                # Normalize and move
                avoid_distance = (avoid_dx**2 + avoid_dy**2)**0.5
                if avoid_distance != 0:
                    move_x = int((avoid_dx / avoid_distance) * MOUSE_SPEED)
                    move_y = int((avoid_dy / avoid_distance) * MOUSE_SPEED)
                    mouse_x += move_x
                    mouse_y += move_y
            else:
                # Random movement when not threatened
                if random.randint(1, 10) == 1:
                    mouse_x += random.choice([-MOUSE_SPEED, 0, MOUSE_SPEED])
                    mouse_y += random.choice([-MOUSE_SPEED, 0, MOUSE_SPEED])

            # Keep the mouse within screen boundaries
            mouse_x = max(0, min(WIDTH - MOUSE_SIZE, mouse_x))
            mouse_y = max(0, min(HEIGHT - MOUSE_SIZE, mouse_y))

            # Save previous cat position
            prev_cat_x, prev_cat_y = cat_x, cat_y

            # Collision detection (cat and mouse)
            cat_rect = pygame.Rect(cat_x, cat_y, CAT_SIZE, CAT_SIZE)
            mouse_rect = pygame.Rect(mouse_x, mouse_y, MOUSE_SIZE, MOUSE_SIZE)

            if cat_rect.colliderect(mouse_rect):
                # Calculate elapsed time and trigger game over
                elapsed_time = round((pygame.time.get_ticks() - start_ticks) / 1000, 2)
                game_over = True

    if game_started:
        # Draw cat and mouse
        screen.blit(cat_img, (cat_x, cat_y))
        screen.blit(mouse_img, (mouse_x, mouse_y))

        if not game_over:
            # Display timer during gameplay
            current_time = round((pygame.time.get_ticks() - start_ticks) / 1000, 2)
            timer_text = small_font.render(f"{current_time} sec", True, TEXT_COLOR)
            screen.blit(timer_text, (10, 10))

    if game_over:
        # Text parts
        text_before = small_font.render("You caught", True, TEXT_COLOR)
        text_after = small_font.render(f"in {elapsed_time} seconds!", True, TEXT_COLOR)

        # Mouse image (small size) for game over screen
        mouse_display = pygame.transform.scale(mouse_img, (30, 30))

        # Calculate X position for centering the result text and image
        total_width = text_before.get_width() + 30 + text_after.get_width()
        start_x = WIDTH // 2 - total_width // 2
        y_pos = HEIGHT // 2 - 20

        # Draw text and image in order
        screen.blit(text_before, (start_x, y_pos))
        screen.blit(mouse_display, (start_x + text_before.get_width() + 5, y_pos))
        screen.blit(text_after, (start_x + text_before.get_width() + 35, y_pos))

        # Retry message
        retry_text = small_font.render("Press SPACE to retry!", True, TEXT_COLOR)
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 30))

    # Update the display and control the frame rate
    pygame.display.update()
    clock.tick(30)

