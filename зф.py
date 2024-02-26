from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, sprite_position_x, sprite_position_y, sprite_width, sprite_height, sprite_speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = sprite_position_x
        self.rect.y = sprite_position_y
        self.width = sprite_width
        self.height = sprite_height
        self.speed = sprite_speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update_right(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < window_height - 80:
            self.rect.y += self.speed
    def update_left(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < window_height - 80:
            self.rect.y += self.speed


font.init()
font = font.Font(None, 35)
lose1 = font.render("Player 1 lose", True, (180, 0, 0))
lose2 = font.render("Player 2 lose", True, (180, 0, 0))
restart_text = font.render("Restart", True, (0, 0, 0))

player1_score = 0
player2_score = 0

speed_y = 3
speed_x = 3

racket1 = Player("racket.png", 30, 200, 50, 150, 4)
racket2 = Player("racket.png", 520, 200, 50, 150, 4)
tennis_ball = GameSprite("tenis_ball.png", 200, 200, 50, 50, 4)

window_height = 500
window_width = 600

background_color = (200, 255, 255)

window = display.set_mode((window_width, window_height))
window.fill(background_color)
finish = False
game = True
restart_button = Rect(250, 300, 100, 50)  # Создаем прямоугольник для кнопки Restart

clock = time.Clock()
FPS = 60

bounce_count = 0
speed_increase = 1  # Задаем начальное значение увеличения скорости

initial_speed_x = speed_x
initial_speed_y = speed_y

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

        # Обработка нажатия на кнопку Restart
        if e.type == MOUSEBUTTONDOWN:
            if restart_button.collidepoint(mouse.get_pos()):
                finish = False  # Сброс значения finish перед новым раундом
                tennis_ball.rect.y = 200
                tennis_ball.rect.x = 200
                bounce_count = 0
                speed_increase = 1
                speed_x = initial_speed_x  # Установка начальной скорости
                speed_y = initial_speed_y  # Установка начальной скорости

    if finish != True:
        window.fill(background_color)
        racket1.reset()
        racket2.reset()
        tennis_ball.reset()

        racket1.update_left()
        racket2.update_right()
        tennis_ball.rect.x += speed_x
        tennis_ball.rect.y += int(speed_y)  # Приводим скорость к целочисленному значению


        if sprite.collide_rect(racket1, tennis_ball) or sprite.collide_rect(racket2, tennis_ball):
            speed_x *= -1
            bounce_count += 1  # Увеличиваем счетчик отскоков
            speed_y *= 1

        if bounce_count >= 3:
            speed_y += 1
            speed_x += 1
            bounce_count -= 3


        if tennis_ball.rect.y > window_height - 50 or tennis_ball.rect.y < 0:
            speed_y *= -1
        if tennis_ball.rect.x < 0:
            finish = True
            player2_score += 1
            window.blit(lose1, (220, 200))
            # Рисуем кнопку Restart
            draw.rect(window, (0, 255, 0), restart_button)
            window.blit(restart_text, (270, 310))

        if tennis_ball.rect.x > window_width:
            finish = True
            player1_score += 1
            window.blit(lose2, (220, 200))
            # Рисуем кнопку Restart
            draw.rect(window, (0, 255, 0), restart_button)
            window.blit(restart_text, (265, 310))

    # Отображаем счетчики побед
    score_text = font.render("" + str(player1_score) + "     " + str(player2_score), True, (0, 0, 0))
    window.blit(score_text, (260, 20))

    display.update()
    clock.tick(FPS)
