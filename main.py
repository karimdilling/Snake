import pygame, sys, random

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

def move_snake():
    for element in snake_body:
        if event.key == pygame.K_UP:
            element.y -= 20
        if event.key == pygame.K_DOWN:
            element.y += 20
        if event.key == pygame.K_LEFT:
            element.x -= 20
        if event.key == pygame.K_RIGHT:
            element.x += 20

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
    if snake_head.colliderect(target_rect):
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
    new_element = pygame.Rect(snake_body_start_3.x + i, snake_body_start_3.y, 20, 20)
    snake_body.append(new_element)
    i += 20

points = 0
i = 20
# start target
target_rect = pygame.Rect(random.randrange(0, WIN_WIDTH, 20), random.randrange(0, WIN_HEIGHT, 20), 20, 20)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            move_snake()
        if event.type == MOVE_SNAKE:
            for element in snake_body:
                element.x -= 20
    
    WINDOW.fill("black")

    draw_snake()
    draw_grid()
    draw_random_target()
    if has_collided_with_target():
        add_to_snake()
        calculate_random_target()
        points += 1
        print(points)
    reenter_if_out_of_window()
    clock.tick(FPS)
    pygame.display.update()