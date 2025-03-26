import pygame
import time
import random
import sqlite3

# Nastavení rychlosti a okna
snake_speed = 15
window_x = 720
window_y = 480

# Inicializace pygame
pygame.init()
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Připojení k databázi
conn = sqlite3.connect('snake_scores.db')
c = conn.cursor()

# Funkce pro vytvoření tabulky a kontrolu, zda existuje sloupec 'name'
def create_table_if_not_exists():
    c.execute("""CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    score INTEGER
                  )""")
    conn.commit()

# Vytvoření tabulky, pokud neexistuje
create_table_if_not_exists()

def save_score(name, score):
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()

def get_high_score():
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 1")
    result = c.fetchone()
    return result  # Vrací jméno a skóre nejlepšího hráče

# Funkce pro zobrazení textu na obrazovce
def show_text(text, font_size, color, x, y):
    font = pygame.font.SysFont('times new roman', font_size)
    text_surface = font.render(text, True, color)
    game_window.blit(text_surface, (x, y))

# Funkce pro získání jména hráče
def get_player_name():
    font = pygame.font.SysFont('times new roman', 30)
    input_box = pygame.Rect(window_x / 4, window_y / 3, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    clock = pygame.time.Clock()

    while True:
        game_window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return text
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        color = color_active if active else color_inactive
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        game_window.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(game_window, color, input_box, 2)

        show_text("Enter your name:", 40, (255, 255, 255), window_x / 4, window_y / 4)
        pygame.display.flip()
        clock.tick(30)

# Výchozí hodnoty hada
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0
paused = False

# Boostovací jablko
boost_fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
boost_fruit_spawn = True
boost_active = False
boost_timer = 0
boost_duration = 50

# Seznam pro překážky
obstacles = []

# Funkce pro generování náhodných překážek
def generate_obstacles(num_obstacles):
    global obstacles
    obstacles = []
    for _ in range(num_obstacles):
        obstacle_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
        obstacles.append(obstacle_position)

# Zobrazení skóre
def show_score():
    font = pygame.font.SysFont('times new roman', 20)
    score_surface = font.render(f'Score: {score}', True, (0, 0, 0))  # Černá barva pro skóre
    game_window.blit(score_surface, (10, 10))

# Konec hry - zobrazení skóre a nejlepšího skóre
def game_over(name):
    save_score(name, score)  # Uložení skóre hráče

    font = pygame.font.SysFont('times new roman', 50)
    game_window.fill((0, 0, 0))  # Černé pozadí

    # Zobrazení aktuálního skóre hráče
    game_over_surface = font.render(f'Your Score: {score}', True, (255, 0, 0))
    game_window.blit(game_over_surface, (window_x / 4, window_y / 4))

    # Získání nejlepšího skóre a jména
    high_score = get_high_score()
    if high_score:
        high_score_text = f"Top Score: {high_score[0]}: {high_score[1]}"
    else:
        high_score_text = "No scores yet."

    high_score_surface = font.render(high_score_text, True, (255, 255, 255))
    game_window.blit(high_score_surface, (window_x / 4, window_y / 3))

    # Pokyny pro hráče
    instructions = pygame.font.SysFont('times new roman', 30)
    exit_text = instructions.render("Press ENTER to play again or ESC to exit", True, (200, 200, 200))
    game_window.blit(exit_text, (window_x / 4, window_y / 2))

    pygame.display.flip()

    # Čekání na stisk klávesy
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart hry
                    main()  # Spuštění nové hry
                elif event.key == pygame.K_ESCAPE:  # Konec hry
                    pygame.quit()
                    quit()

    # Čekání na stisk klávesy
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart hry
                    main()  # Spuštění nové hry
                elif event.key == pygame.K_ESCAPE:  # Konec hry
                    pygame.quit()
                    quit()
    
    # Získání nejlepšího skóre a jména
    high_score = get_high_score()
    if high_score:
        name_text = f"Top Score: {high_score[0]}: {high_score[1]}"
    else:
        name_text = "No scores yet."
    
    score_surface = font.render(name_text, True, (255, 255, 255))
    game_window.blit(score_surface, (window_x / 4, window_y / 3))
    
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Herní smyčka
name = get_player_name()  # Získání jména hráče na začátku hry
generate_obstacles(5)  # Generování 5 překážek na začátku hry

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'
            elif event.key == pygame.K_SPACE:
                paused = not paused
    
    if paused:
        continue
    
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'
    
    if direction == 'UP':
        snake_position[1] -= 10
    elif direction == 'DOWN':
        snake_position[1] += 10
    elif direction == 'LEFT':
        snake_position[0] -= 10
    elif direction == 'RIGHT':
        snake_position[0] += 10
    
    snake_body.insert(0, list(snake_position))
    if snake_position == fruit_position:
        score += 10 if not boost_active else 20
        fruit_spawn = False
    else:
        snake_body.pop()
    
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    fruit_spawn = True
    
    if snake_position == boost_fruit_position:
        boost_active = True
        boost_timer = boost_duration
        boost_fruit_spawn = False
    
    if not boost_fruit_spawn:
        boost_fruit_position = [random.randrange(1, (window_x // 10)) * 10, random.randrange(1, (window_y // 10)) * 10]
    boost_fruit_spawn = True
    
    if boost_active:
        snake_speed = 25
        boost_timer -= 1
        if boost_timer <= 0:
            boost_active = False
            snake_speed = 15
    
    game_window.fill((0, 255, 0))  # Zelené pozadí
    for pos in snake_body:
        pygame.draw.rect(game_window, (128, 0, 128), pygame.Rect(pos[0], pos[1], 10, 10))  # Fialový had
    pygame.draw.rect(game_window, (255, 0, 0), pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
    pygame.draw.rect(game_window, (0, 0, 255), pygame.Rect(boost_fruit_position[0], boost_fruit_position[1], 10, 10))
    
    # Zobrazení překážek
    for obstacle in obstacles:
        pygame.draw.rect(game_window, (0, 0, 0), pygame.Rect(obstacle[0], obstacle[1], 10, 10))  # Černé překážky
    
    if snake_position[0] < 0 or snake_position[0] >= window_x or snake_position[1] < 0 or snake_position[1] >= window_y:
        game_over(name)
    
    for block in snake_body[1:]:
        if snake_position == block:
            game_over(name)
    
    # Kontrola kolize s překážkou
    for obstacle in obstacles:
        if snake_position == obstacle:
            game_over(name)
    
    show_score()
    pygame.display.update()
    fps.tick(snake_speed)
