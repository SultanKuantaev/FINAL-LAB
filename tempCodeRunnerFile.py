import pygame
import sys
import random
import psycopg2

pygame.init()

# Задаем размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Определение цветов
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Начальное положение змеи, скорость, еда, счет и уровень
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]
food = {'pos': [0, 0], 'weight': 1, 'spawn_time': 0}
food_spawn = True
score = 0
level = 1
speed_increase = 0.1  # Увеличение скорости за каждый уровень
food_counter = 0  

fps = pygame.time.Clock()

# Function to insert the player's name and score into the database
# Function to insert the player's name and score into the database
# Function to insert the player's name, score, and level into the database
def insert_score(name, score, level):
    conn = psycopg2.connect(
        dbname='postgres',  # replace with your database name
        user='postgres',    # replace with your username
        password='1234',    # replace with your password
        host='localhost',   # replace with your host
        port='5432'         # replace with your port if it's not the default
    )
    cur = conn.cursor()
    # SQL query to insert the new score and level
    insert_query = "INSERT INTO snake_game_scores (player_name, score, level) VALUES (%s, %s, %s)"
    cur.execute(insert_query, (name, score, level))
    conn.commit()
    cur.close()
    conn.close()


# Prompt for the player's name before the game starts
player_name = input("Enter your name: ")
player_name = player_name.encode('utf-8', 'ignore').decode('utf-8')
# Функция проверки столкновений
def check_collision(pos):
    if pos[0] < 0 or pos[0] > SCREEN_WIDTH - 10 or pos[1] < 0 or pos[1] > SCREEN_HEIGHT - 10:
        return True
    if pos in snake_pos[1:]:
        return True
    return False

# Функция для генерации новой еды
def get_random_food():
    global food_counter
    while True:
        pos = [random.randrange(1, (SCREEN_WIDTH // 10)) * 10, random.randrange(1, (SCREEN_HEIGHT // 10)) * 10]
        if pos not in snake_pos:
            weight = 2 if food_counter >= 2 else 1
            food_counter = 0 if weight == 2 else food_counter + 1
            return {'pos': pos, 'weight': weight, 'spawn_time': pygame.time.get_ticks()}

# Главный игровой цикл
try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_speed[1] == 0:
                    snake_speed = [0, -10]
                elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                    snake_speed = [0, 10]
                elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                    snake_speed = [-10, 0]
                elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                    snake_speed = [10, 0]

        snake_pos.insert(0, list(map(lambda x, y: x + y, snake_pos[0], snake_speed)))

        # In your game loop, when the game ends
                if check_collision(snake_pos[0]):
                    insert_score(player_name, score, level)  # Include level here
                    pygame.quit()
                    sys.exit()


        if snake_pos[0] == food['pos']:
            score += food['weight']
            if score % 3 == 0:
                level += 1
                fps.tick(10 + level * speed_increase)
            food_spawn = True
        else:
            snake_pos.pop()

        if food_spawn:
            food = get_random_food()
            food_spawn = False

        current_time = pygame.time.get_ticks()
        if current_time - food['spawn_time'] > 10000:
            food_spawn = True

        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        food_color = RED if food['weight'] == 1 else (255, 165, 0)
        pygame.draw.rect(screen, food_color, pygame.Rect(food['pos'][0], food['pos'][1], 10, 10))

        font = pygame.font.SysFont('arial', 20)
        score_text = font.render(f"Score: {score} Level: {level}", True, WHITE)
        screen.blit(score_text, [0, 0])

        pygame.display.flip()
        fps.tick(10 + level * speed_increase)
except SystemExit:
    pygame.quit()
