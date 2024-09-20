import pygame
import sys

pygame.init()

# Параметры окна
WIDTH, HEIGHT = 640, 480
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Trapped Maze")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


# Класс для игрока
class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.lives = 3  # Добавляем жизни

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def draw(self, window):
        pygame.draw.rect(window, BLUE, self.rect)
        # Отображаем количество жизней
        font = pygame.font.Font(None, 36)
        text = font.render(f"Lives: {self.lives}", True, BLACK)
        window.blit(text, (10, 50))  # Выводим количество жизней

class MovingTrap:
    def __init__(self, x, y, width, height, direction, speed, boundary_start, boundary_end):
        self.rect = pygame.Rect(x, y, width, height)
        self.direction = direction  # 'horizontal' или 'vertical'
        self.speed = speed
        self.boundary_start = boundary_start
        self.boundary_end = boundary_end

    def move(self):
        if self.direction == 'horizontal':
            self.rect.x += self.speed
            # Меняем направление при достижении границ
            if self.rect.x <= self.boundary_start or self.rect.x >= self.boundary_end:
                self.speed = -self.speed
        elif self.direction == 'vertical':
            self.rect.y += self.speed
            # Меняем направление при достижении границ
            if self.rect.y <= self.boundary_start or self.rect.y >= self.boundary_end:
                self.speed = -self.speed

    def draw(self, window):
        pygame.draw.rect(window, GREEN, self.rect)  # Движущиеся ловушки тоже зеленые


# Класс для лабиринта (с возможностью смены уровней)
# Класс лабиринта с обычными и движущимися ловушками
class Maze:
    def __init__(self, level=1):
        self.level = level
        self.load_level(level)

    def load_level(self, level):
        if level == 1:
            self.walls = [
                pygame.Rect(100, 100, 50, 200),
                pygame.Rect(200, 150, 300, 50),
                pygame.Rect(50, 300, 400, 50)
            ]
            self.traps = [
                pygame.Rect(250, 250, 40, 40),
                pygame.Rect(400, 200, 40, 40)
            ]
            # Движущиеся ловушки
            self.moving_traps = [
                MovingTrap(300, 150, 40, 40, 'horizontal', 2, 300, 500),
                MovingTrap(100, 350, 40, 40, 'vertical', 3, 100, 300)
            ]
        elif level == 2:
            self.walls = [
                pygame.Rect(150, 100, 200, 50),
                pygame.Rect(350, 200, 50, 200),
                pygame.Rect(100, 350, 400, 50)
            ]
            self.traps = [
                pygame.Rect(300, 300, 40, 40),
                pygame.Rect(150, 200, 40, 40)
            ]
            self.moving_traps = [
                MovingTrap(200, 250, 40, 40, 'vertical', 4, 200, 400),
                MovingTrap(350, 150, 40, 40, 'horizontal', 2, 150, 500)
            ]
        self.exit = pygame.Rect(580, 430, 50, 50)

    def draw(self, window):
        for wall in self.walls:
            pygame.draw.rect(window, (0, 0, 0), wall)
        pygame.draw.rect(window, (255, 0, 0), self.exit)
        for trap in self.traps:
            pygame.draw.rect(window, (0, 255, 0), trap)
        for moving_trap in self.moving_traps:
            moving_trap.draw(window)

    def move_traps(self):
        for moving_trap in self.moving_traps:
            moving_trap.move()


# Класс для таймера
class Timer:
    def __init__(self):
        self.start_ticks = pygame.time.get_ticks()

    def draw(self, window):
        # Подсчет времени (секунды)
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
        font = pygame.font.Font(None, 36)
        text = font.render(f"Time: {elapsed_time}", True, BLACK)
        window.blit(text, (10, 10))

class Score:
    def __init__(self):
        self.points = 0

    def add_points(self, points):
        self.points += points

    def draw(self, window):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {self.points}', True, (0, 0, 0))
        window.blit(score_text, (10, 10))  # Отрисовка очков в верхнем левом углу

# Основной игровой цикл
def game_loop():
    clock = pygame.time.Clock()
    player = Player(50, 50, 40, 40)  # Начальная позиция игрока
    level = 1  # Уровень игры начинаем с 1
    maze = Maze(level)
    timer = Timer()  # Создание таймера
    score = Score()  # Создание счетчика очков

    while True:
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Движение игрока
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Движение ловушек
        maze.move_traps()  # <-- Добавляем движение ловушек здесь

        # Проверка столкновений с лабиринтом
        for wall in maze.walls:
            if player.rect.colliderect(wall):
                # Вернуть игрока назад при столкновении
                if keys[pygame.K_LEFT]:
                    player.rect.x += player.speed
                if keys[pygame.K_RIGHT]:
                    player.rect.x -= player.speed
                if keys[pygame.K_UP]:
                    player.rect.y += player.speed
                if keys[pygame.K_DOWN]:
                    player.rect.y -= player.speed

        # Проверка столкновений с ловушками
        for trap in maze.traps:
            if player.rect.colliderect(trap):
                 player.lives -= 1  # Уменьшение жизней при столкновении
                 print(f"Попали в ловушку! Осталось жизней: {player.lives}")
                 player.rect.x, player.rect.y = 50, 50
                 score.add_points(-50)  # Вычитаем 50 очков при попадании в ловушку

                 if player.lives == 0:
                     print("Игра окончена!")
                     pygame.quit()
                     sys.exit()

        # Проверка столкновений с движущимися ловушками
        for moving_trap in maze.moving_traps:
            if player.rect.colliderect(moving_trap.rect):
                 player.lives -= 1
                 print(f"Попали в движущуюся ловушку! Осталось жизней: {player.lives}")
                 player.rect.x, player.rect.y = 50, 50
                 score.add_points(-50)  # Вычитаем 50 очков при попадании в движущуюся ловушку

                 if player.lives == 0:
                     print("Игра окончена!")
                     pygame.quit()
                     sys.exit()

        # Проверка выхода из лабиринта
        if player.rect.colliderect(maze.exit):
            print(f"Уровень {level} пройден!")
            score.add_points(100)  # Добавляем 100 очков за прохождение уровня
            level += 1
            if level > 2:  # Допустим, у нас два уровня
                print("Поздравляю, игра пройдена!")
                pygame.quit()
                sys.exit()
            else:
                 maze = Maze(level)  # Загрузить следующий уровень
                 player.rect.x, player.rect.y = 50, 50  # Возвращаем игрока на старт

        # Отрисовка
        WINDOW.fill(WHITE)
        player.draw(WINDOW)
        maze.draw(WINDOW)
        score.draw(WINDOW)  # Отрисовка очков на экране
        timer.draw(WINDOW)  # Отрисовка таймера
        pygame.display.flip()
        clock.tick(30)

# Запуск игры
if __name__ == "__main__":
    game_loop()
