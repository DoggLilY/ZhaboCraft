import block
import pygame

pygame.init()

# Use a system font (Arial) with size 48
font = pygame.font.SysFont("Arial", 24)

# Screen dimensions
w, h = 800, 600
win = pygame.display.set_mode((w, h))

pygame.display.set_caption("ЖАБОКРАФТ")

def loop():
    run = True
    clock = pygame.time.Clock()

    # Initial player coordinates
    player_x, player_y = 13, 13

    # Key press states to handle press-and-hold behavior
    key_left_pressed = False
    key_right_pressed = False
    key_up_pressed = False
    key_down_pressed = False

    while run:
        clock.tick(30)  # Frame rate: 30 FPS

        # Event handling
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()

        # Movement logic
        if keys[pygame.K_a]:
            if not key_left_pressed:
                player_x -= 1
                key_left_pressed = True
        else:
            key_left_pressed = False

        if keys[pygame.K_d]:
            if not key_right_pressed:
                player_x += 1
                key_right_pressed = True
        else:
            key_right_pressed = False

        if keys[pygame.K_w]:
            if not key_up_pressed:
                player_y -= 1
                key_up_pressed = True
        else:
            key_up_pressed = False

        if keys[pygame.K_s]:
            if not key_down_pressed:
                player_y += 1
                key_down_pressed = True
        else:
            key_down_pressed = False

        # Clear the screen
        win.fill((0, 0, 0))

        # Get coordinates for drawing
        x, y = getXYforM()

        # Draw chunks and player
        block.chunk.drawchunkson(win, w, h, player_x, player_y)
        win.blit(block.frog.sprite, (w / 2 - 24, h / 2 - 24))

        # Draw black bars on the sides
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 100, 600))  # Left bar
        pygame.draw.rect(win, (0, 0, 0), (700, 0, 100, 600))  # Right bar

        # Display player coordinates
        printfont((0, 0), str(player_x - 13) + ", " + str(player_y - 13))
        printfont((0, 0), str(player_x - 13) + ", " + str(player_y - 13))

        # Update the screen
        pygame.display.update()

    pygame.quit()

def getXYforM():
    return (w // 2 - 48 * 6.5, h // 2 - 48 * 6.5)

def printfont(pos: tuple, text: str):
    rend = font.render(text, False, (255, 255, 255))  # Render text in white
    win.blit(rend, pos)

if __name__ == "__main__":
    # Initialize chunks
    block.chunk.generate((0, 0))
    loop()
