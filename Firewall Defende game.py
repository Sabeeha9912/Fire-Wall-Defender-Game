import pygame
import random
import sys

# -------------------------------------------------------------------------
# 1. INITIALIZATION & SETUP
# -------------------------------------------------------------------------
pygame.init()
pygame.mixer.init()  # Controls game audio systems

# Screen Setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Firewall Defender")

clock = pygame.time.Clock()  # Controls frame rate (FPS)

# -------------------------------------------------------------------------
# 2. ASSETS LOADING (IMAGES & SOUNDS)
# -------------------------------------------------------------------------
try:
    # Load and scale game graphics
    bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
    game_over_bg = pygame.transform.scale(pygame.image.load('game_over_screen.png'), (WIDTH, HEIGHT))
    player_img = pygame.transform.scale(pygame.image.load('player_icon.png'), (80, 80))
    
    img_safe = pygame.transform.scale(pygame.image.load('safe_icon.png'), (40, 40))
    img_virus = pygame.transform.scale(pygame.image.load('virus_icon.png'), (40, 40))
    img_unknown = pygame.transform.scale(pygame.image.load('unknown_icon.png'), (40, 40))
    
    # Audio Setup
    virus_sound = pygame.mixer.Sound('virus_alert.wav')
    safe_sound = pygame.mixer.Sound('safe_sound.wav')
    game_over_sound = pygame.mixer.Sound('game_over.wav')
    
    pygame.mixer.music.load('background.wav')
    pygame.mixer.music.play(-1)  # -1 means loop infinitely
    
except pygame.error as error:
    print(f"Asset Error: {error}. Make sure all assets are in the same folder.")
    pygame.quit()
    sys.exit()

# List for randomly picking falling packets
packet_choices = [img_safe, img_virus, img_unknown]

# -------------------------------------------------------------------------
# 3. GAME STATE VARIABLES
# -------------------------------------------------------------------------
# Player dimensions and positioning
player_rect = pygame.Rect(WIDTH // 2, HEIGHT - 90, 80, 80)

# Main gameplay stats
score = 0
lives = 5
packets = []          # Holds active packets running down the screen
game_over = False

# Hint tracking mechanics
hints_left = 3
hint_msg = ""
hint_timer = 0        # Dictates how long (in frames) the hint text displays

# Colors
ui_font = pygame.font.SysFont('Arial', 24)
hint_font = pygame.font.SysFont('Arial', 36, bold=True)

# Custom fonts to match your background box styling perfectly
final_score_font = pygame.font.SysFont('Consolas', 42, bold=True)
instructions_font = pygame.font.SysFont('Arial', 20, bold=False)

CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Load High Score
try:
    with open("highscore.txt", "r") as file:
        high_score = int(file.read())
except:
    high_score = 0  # Default value if file doesn't exist yet

# -------------------------------------------------------------------------
# 4. MAIN PROGRAM LOOP
# -------------------------------------------------------------------------
running = True
while running:
    
    # --- A. EVENT TRACKING & INPUTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Key controls specifically for when the game is actively running
        if not game_over and event.type == pygame.KEYDOWN:
            # Trigger hint system when pressing 'H'
            if event.key == pygame.K_h and hints_left > 0:
                # Filter out only the safe green packets on screen
                safe_packets = [p for p in packets if p[1] == img_safe]
                
                if safe_packets:
                    # Target the lowest safe packet on the screen (highest Y coordinate)
                    closest_target = max(safe_packets, key=lambda p: p[0].y)
                    
                    if closest_target[0].x > player_rect.x:
                        hint_msg = "MOVE RIGHT!"
                    else:
                        hint_msg = "MOVE LEFT!"
                        
                    hints_left -= 1
                    hint_timer = 90  # Keeps prompt up for ~1.5 seconds at 60fps
                else:
                    hint_msg = "No safe packets visible!"
                    hint_timer = 60  # Short warning message display duration

        # Key controls specifically for the Game Over screen
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:    # Restart Routine
                score = 0
                lives = 5
                hints_left = 3
                hint_msg = ""
                hint_timer = 0
                packets.clear()
                player_rect.x = WIDTH // 2
                game_over = False
                pygame.mixer.music.play(-1)
                
            elif event.key == pygame.K_q:  # Quit action
                running = False

    # --- B. GAMEPLAY LOGIC (ACTIVE STATE) ---
    if not game_over:
        # Player Movement Control (A/D or Arrow Keys)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_rect.x > 0:
            player_rect.x -= 7
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_rect.x < WIDTH - player_rect.width:
            player_rect.x += 7

        # Random Spawner Logic
        if random.randint(1, 25) == 1:
            random_x = random.randint(0, WIDTH - 40)
            new_packet_rect = pygame.Rect(random_x, -40, 40, 40)
            chosen_texture = random.choice(packet_choices)
            packets.append([new_packet_rect, chosen_texture])

        # Managing Falling Objects & Intersections
        for pkt in packets[:]:
            pkt[0].y += 5  # Push objects downward
            
            # Handling Collisions
            if pkt[0].colliderect(player_rect):
                if pkt[1] == img_safe:
                    score += 1
                    safe_sound.play()
                elif pkt[1] == img_virus:
                    lives -= 1
                    if lives > 0: virus_sound.play()
                else:
                    # Unknown data risk calculation (50/50 split odds)
                    if random.randint(0, 1) == 1:
                        score += 1
                        safe_sound.play()
                    else:
                        lives -= 1
                        if lives > 0: virus_sound.play()
                
                packets.remove(pkt)
                
            # Clean up elements passing off-screen boundaries
            elif pkt[0].y > HEIGHT:
                packets.remove(pkt)

        # Record high score updates dynamically
        if score > high_score:
            high_score = score

        # Evaluate failure metrics
        if lives <= 0:
            game_over = True
            pygame.mixer.music.stop()
            game_over_sound.play()

        # --- C. RENDERING SCENE ---
        screen.blit(bg, (0, 0))
        screen.blit(player_img, player_rect)
        
        for pkt in packets:
            screen.blit(pkt[1], pkt[0])

        # Formatting standard text interfaces
        txt_score = ui_font.render(f"Score: {score}", True, WHITE)
        txt_lives = ui_font.render(f"Lives: {lives}", True, (255, 50, 50) if lives == 1 else WHITE)
        txt_hints = ui_font.render(f"Hints [H]: {hints_left}", True, YELLOW)
        txt_highscore = ui_font.render(f"High Score: {high_score}", True, CYAN)

        screen.blit(txt_score, (20, 20))
        screen.blit(txt_lives, (20, 50))
        screen.blit(txt_hints, (20, 80))
        screen.blit(txt_highscore, (WIDTH - 200, 20))

        # Render direction alert prompt overlay if active
        if hint_timer > 0:
            surf_hint_alert = hint_font.render(hint_msg, True, YELLOW)
            x_centered = WIDTH // 2 - surf_hint_alert.get_width() // 2
            screen.blit(surf_hint_alert, (x_centered, HEIGHT - 180))
            hint_timer -= 1

    # --- D. RENDERING GAME OVER STATE ---
    else:
        screen.blit(game_over_bg, (0, 0))

        # Render numbers
        surf_final_score = final_score_font.render(str(score), True, CYAN)
        surf_final_high = final_score_font.render(str(high_score), True, CYAN)
        
    
        # Mathematical alignment calculations to perfectly center numbers inside the graphic frames:
        # Box horizontal center for 'SCORE' number is roughly at X=615
        score_x = 615 - (surf_final_score.get_width() // 2)
        # Box horizontal center for 'HIGH SCORE' number is roughly at X=615
        high_x = 615 - (surf_final_high.get_width() // 2)

        # Apply calculated coordinates
        screen.blit(surf_final_score, (score_x, 268))
        screen.blit(surf_final_high, (high_x, 336))

    # Synchronize layout updates
    pygame.display.flip()
    clock.tick(60)

# -------------------------------------------------------------------------
# 5. SHUTDOWN LOGIC
# -------------------------------------------------------------------------
# Record tracking scores data locally to disk before program exits
with open("highscore.txt", "w") as file:
    file.write(str(high_score))

pygame.quit()
sys.exit()