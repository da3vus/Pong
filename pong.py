import pygame
import random

pygame.init()  # Initialize pygame

# Window size
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 700
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Game title on top of window
pygame.display.set_caption("Pong")

# Text font
font = pygame.font.SysFont("Comic Sans", 50, True, False)

# Clock for delay/frame rate
clock = pygame.time.Clock()

# Score variables for player and opponent
player_score = 0
opp_score = 0

# Colors for the shapes/text being drawn
white = (255, 255, 255)
grey = (128, 128, 128)

# Create player and opponent paddles
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 110
player_speed = 7.5
player = pygame.Rect(50, 50, PADDLE_WIDTH, PADDLE_HEIGHT)
player.center = (50, WINDOW_HEIGHT / 2)  # Align paddle to center of left side screen

opp_speed = 8
opp = pygame.Rect(WINDOW_WIDTH - 50, 50, PADDLE_WIDTH, PADDLE_HEIGHT)
opp.center = (WINDOW_WIDTH - 50, WINDOW_HEIGHT / 2)  # Align paddle to center of right side screen

# Create ball
BALL_WIDTH = 16
BALL_HEIGHT = 16
ball_speed_x = 7
ball_speed_y = 7
ball = pygame.Rect(100, 100, BALL_WIDTH, BALL_HEIGHT)
ball.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)  # Make the ball appear at the center of the screen


# Function to respawn ball after a side has scored
def respawnBall():
    global ball_speed_x, ball_speed_y

    # Respawn the ball at the center of the screen
    ball.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    # Choose a random direction for the ball to travel (either 1 or -1) or left/right
    ball_speed_x *= (random.randint(0, 1) * 2) - 1
    ball_speed_y *= (random.randint(0, 1) * 2) - 1


# Function to handle collision between the ball and player/opponent paddles
def ballCollision(paddle):
    global ball_speed_x, ball_speed_y

    # When the ball collides with the top of the paddle, where the bottom of the ball is at or
    # below the top of paddle and when the top of the ball is above the top of the paddle.
    if ball.bottom >= paddle.top > ball.top:
        # Make the y direction negative so ball always bounces upwards off the top of paddle
        ball_speed_y = -abs(ball_speed_y)

    # When the ball collides with the bottom of the paddle, where the top of the ball is at or above the
    # bottom of the paddle and when the bottom of the ball is below the bottom of the paddle.
    elif ball.top <= paddle.bottom < ball.bottom:
        # Make the y direction positive so ball always bounces downward off the bottom of paddle
        ball_speed_y = abs(ball_speed_y)

    # When the ball collides with the side of the paddle
    else:
        # Change x direction of ball to bounce the opposite way
        ball_speed_x *= -1


# Function to redraw the game window to update display while running
def redrawWindow():
    # Fill window when drawing too, so we can see the shapes move properly
    window.fill((0, 0, 0))  # Window black background

    # Set the text for player and opponent scores
    player_text = font.render(str(player_score), 1, white)
    window.blit(player_text, (WINDOW_WIDTH / 4, 20))

    opp_text = font.render(str(opp_score), 1, white)
    window.blit(opp_text, (3 * (WINDOW_WIDTH / 4), 20))

    # Draw line in center of screen
    pygame.draw.line(window, grey, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 1)

    # Draw the player/opponent paddles and ball
    pygame.draw.rect(window, white, player)
    pygame.draw.rect(window, white, opp)
    pygame.draw.ellipse(window, white, ball)  # Make the ball round by using ellipse instead of rect
    pygame.display.update()  # Update display


# While loop runs the game while true
run = True
while run:
    # Close game when clicking x button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()  # Get the list of keys pressed

    # Up arrow key moves the player paddle up
    if keys[pygame.K_UP]:
        # Top of rectangle collides with top of the screen (where coordinate is 0)
        if player.top > 0:
            player.y -= player_speed

    # Down arrow key moves the player paddle down
    if keys[pygame.K_DOWN]:
        # Bottom of rectangle collides with bottom of screen (where coordinate is max height of window)
        if player.bottom < WINDOW_HEIGHT:
            player.y += player_speed

    # Opponent AI movement:
    # When ball is above top of opponent paddle, opponent moves up
    if ball.y <= opp.top:
        opp.y -= opp_speed
    # When ball is below bottom of opponent paddle, opponent moves down
    if ball.y >= opp.bottom:
        opp.y += opp_speed

    # When ball collides with player/opponent paddles
    if ball.colliderect(player):
        ballCollision(player)
    if ball.colliderect(opp):
        ballCollision(opp)

    # Change y direction of ball when colliding with top or bottom of screen
    if ball.bottom >= WINDOW_HEIGHT or ball.top <= 0:
        ball_speed_y *= -1

    # When ball collides with left side of window, opponent scores
    if ball.left <= 0:
        opp_score += 1  # Increment opponent score by 1
        respawnBall()  # Respawn ball after scoring

    # When ball collides with right side of window, player scores
    if ball.right >= WINDOW_WIDTH:
        player_score += 1  # Increment player score by 1
        respawnBall()  # Respawn ball after scoring

    # Initiate ball to move by applying speed values to x and y positions
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    redrawWindow()  # Redraw window to update display
    clock.tick(80)  # Clock for frame rate

pygame.quit()  # Quit pygame when game finishes
