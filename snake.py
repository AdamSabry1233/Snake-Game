# Import necessary libraries
import pygame
import random
import time


# Initialize Pygame
pygame.init()

# Set up the game screen dimensions
width, height = 400, 400
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Initial position and movement direction of the snake
x, y = 200, 200
delta_x, delta_y = 10, 0

# Initial position of the food
food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10

# Initialize the snake body
body_list = [(x, y)]

# Set up the game clock
clock = pygame.time.Clock()

# Flag to track if the game is over
game_over = False

# Set up the font for displaying score and messages
font = pygame.font.SysFont('bahnschrift', 25)


# Function to reset the game state
def reset_game():
    global x, y, food_x, food_y, game_over, body_list, delta_x, delta_y
    x, y = 200, 200
    delta_x, delta_y = 10, 0
    food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10
    body_list = [(x, y)]
    game_over = False


# Function to update the snake's position and check for collisions
def snake():
    global x, y, food_x, food_y, game_over
    x = (x + delta_x) % width
    y = (y + delta_y) % height

    # Check for collisions with the snake's body
    if (x, y) in body_list:
        game_over = True
        return

    # Append the current position to the snake's body
    body_list.append((x, y))

    # Check for collision with food
    if food_x == x and food_y == y:
        while (food_x, food_y) in body_list:
            food_x, food_y = random.randrange(0, width) // 10 * 10, random.randrange(0, height) // 10 * 10
    else:
        # If no collision with food, remove the tail segment
        del body_list[0]

    # Draw the game screen
    game_screen.fill((0, 0, 0))
    score = font.render("Score:" + str(len(body_list)), True, (255, 255, 0))
    game_screen.blit(score, [0, 0])
    pygame.draw.rect(game_screen, (255, 0, 0), [food_x, food_y, 10, 10])
    for (i, j) in body_list:
        pygame.draw.rect(game_screen, (255, 255, 255), [i, j, 10, 10])
    pygame.display.update()


# Main game loop
while True:
    # Check if the game is over
    if game_over:
        # Display game over message and prompt to restart
        game_screen.fill((0, 0, 0))
        score = font.render("Score:" + str(len(body_list)), True, (255, 255, 0))
        game_screen.blit(score, [0, 0])
        msg = font.render("Game Over! Press 'R' to restart", True, (255, 255, 50))
        game_screen.blit(msg, [width // 13, height // 13])
        pygame.display.update()

        # Event handling for restart
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()

        #time.sleep(60)  # Change the duration (in seconds) as needed

      #  pygame.quit()
        #quit()

        # Skip the rest of the loop if the game is over
        continue

    # Event handling for user input
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if delta_x != 10:
                    delta_x = -10
                delta_y = 0
            elif event.key == pygame.K_RIGHT:
                if delta_x != -10:
                    delta_x = 10
                delta_y = 0
            elif event.key == pygame.K_UP:
                delta_x = 0
                if delta_y != 10:
                    delta_y = -10
            elif event.key == pygame.K_DOWN:
                delta_x = 0
                if delta_y != -10:
                    delta_y = 10
            else:
                continue
            snake()

    # If no events, update snake position
    if not events:
        snake()

    # Control the game speed
    clock.tick(20)