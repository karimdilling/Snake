import pygame, sys, random

from pygame.constants import USEREVENT

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
FPS = 60

# snake head and 3 body start elements
snake_head = pygame.Rect(300, 300, 20, 20)
snake_body_start_1 = pygame.Rect(320, 300, 20, 20)
snake_body_start_2 = pygame.Rect(340, 300, 20, 20)
snake_body_start_3 = pygame.Rect(360, 300, 20, 20)
snake_body = [snake_head, snake_body_start_1, snake_body_start_2, snake_body_start_3]

def draw_grid():
    for x_coord in range(20, WIN_WIDTH, 20):
        pygame.draw.line(WINDOW, "grey", (x_coord, 0), (x_coord, WIN_HEIGHT))
    for y_coord in range(20, WIN_HEIGHT, 20):
        pygame.draw.line(WINDOW, "grey", (0, y_coord), (WIN_WIDTH, y_coord))

def draw_snake():
    pygame.draw.rect(WINDOW, "darkgreen", snake_head)
    for element in snake_body:
        pygame.draw.rect(WINDOW, "green", element)

# boolean values to check for the snake not running into itself
can_move_left = True
can_move_right = True
can_move_up = True
can_move_down = True

def move_snake():
    global direction, can_move_left, can_move_right, can_move_up, can_move_down
    if direction == "left":
        new_snake_head = snake_body.pop()
        new_snake_head.x = snake_body[0].x - 20
        new_snake_head.y = snake_body[0].y
        snake_body.insert(0, new_snake_head)
        can_move_right = False
        can_move_down = True
        can_move_up = True
    if direction == "right":
        new_snake_head = snake_body.pop()
        new_snake_head.x = snake_body[0].x + 20
        new_snake_head.y = snake_body[0].y
        snake_body.insert(0, new_snake_head)
        can_move_left = False
        can_move_down = True
        can_move_up = True
    if direction == "up":
        new_snake_head = snake_body.pop()
        new_snake_head.x = snake_body[0].x
        new_snake_head.y = snake_body[0].y - 20
        snake_body.insert(0, new_snake_head)
        can_move_down = False
        can_move_left = True
        can_move_right = True
    if direction == "down":
        new_snake_head = snake_body.pop()
        new_snake_head.x = snake_body[0].x
        new_snake_head.y = snake_body[0].y + 20
        snake_body.insert(0, new_snake_head)
        can_move_up = False
        can_move_left = True
        can_move_right = True

# timer to auto move snake
MOVE_SNAKE = pygame.USEREVENT
pygame.time.set_timer(MOVE_SNAKE, 200)

def calculate_random_target():
    global target_rect
    random_x_coord = random.randrange(0, WIN_WIDTH, 20)
    random_y_coord = random.randrange(0, WIN_HEIGHT, 20)
    target_rect = pygame.Rect(random_x_coord, random_y_coord, 20, 20)

def draw_random_target():
    pygame.draw.rect(WINDOW, "red", target_rect)

def has_collided_with_target():
    if snake_body[0].colliderect(target_rect):
        return True
    return False

def has_collided_with_itself():
    for i in range(1, len(snake_body)):
        if snake_body[0].colliderect(snake_body[i]):
            return True
    return False

# when snake leaves the screen it reenters it from the other side
def reenter_if_out_of_window():
    for element in snake_body:
        if element.x < 0:
            element.x = WIN_WIDTH - 20
        if element.x >= WIN_WIDTH:
            element.x = 0
        if element.y < 0:
            element.y = WIN_HEIGHT - 20
        if element.y >= WIN_HEIGHT:
            element.y = 0

def add_to_snake():
    global i
    if direction == "left":
        new_element = pygame.Rect(snake_body[len(snake_body) - 1].x + i, snake_body[len(snake_body) - 1].y, 20, 20)
    if direction == "right":
        new_element = pygame.Rect(snake_body[len(snake_body) - 1].x - i, snake_body[len(snake_body) - 1].y, 20, 20)
    if direction == "up":
        new_element = pygame.Rect(snake_body[len(snake_body) - 1].x, snake_body[len(snake_body) - 1].y + i, 20, 20)
    if direction == "down":
        new_element = pygame.Rect(snake_body[len(snake_body) - 1].x, snake_body[len(snake_body) - 1].y - 20, 20, 20)
    snake_body.append(new_element)
    i += 20

# define fonts
score_font = pygame.font.SysFont(None, 40)
game_over_font = pygame.font.SysFont(None, 80)

def show_score():
    score_surface = score_font.render(f"Score: {points}", False, "orange")
    WINDOW.blit(score_surface, (10, 10))

def show_game_over():
    game_over_surface = game_over_font.render("Game Over", True, "red")
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.center = (WIN_WIDTH / 2, WIN_HEIGHT / 2)
    WINDOW.blit(game_over_surface, game_over_rect)

points = 0
i = 20
direction = "left"
# start target
target_rect = pygame.Rect(random.randrange(0, WIN_WIDTH, 20), random.randrange(0, WIN_HEIGHT, 20), 20, 20)
game_over = False

running = True
while running:
    if game_over == True:
        pygame.time.delay(2000)
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and can_move_up:
                direction = "up"
            if event.key == pygame.K_DOWN and can_move_down:
                direction = "down"
            if event.key == pygame.K_LEFT and can_move_left:
                direction = "left"
            if event.key == pygame.K_RIGHT and can_move_right:
                direction = "right"
        if event.type == MOVE_SNAKE:
            move_snake()
            WINDOW.fill("black")
            draw_random_target()
            draw_snake()
            draw_grid()
            if has_collided_with_target():
                add_to_snake()
                calculate_random_target()
                points += 1
            reenter_if_out_of_window()
            if has_collided_with_itself():
                show_game_over()
                game_over = True

    show_score()
    clock.tick(FPS)
    pygame.display.update()