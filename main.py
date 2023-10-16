import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import pyray
from raylib import colors
import random
import math
import time  # Добавляем модуль time

class Ball:
    def __init__(self, width, height):
        self.x = width - random.randint(50, 750)
        self.y = height - random.randint(400, 550)
        self.randX = random.choice([-1, 1])
        self.randY = random.choice([-1, 1])
        self.speed_x = random.choice([2, 3, 4]) * self.randX
        self.speed_y = random.choice([2, 3, 4]) * self.randY
        self.texture = pyray.load_texture("ball.png")

    def update(self, width, height):
        if self.x + 50 > width or self.x - 50 < 0:
            self.speed_x = -self.speed_x
        if self.y - 50 < 0:
            self.speed_y = -self.speed_y

        self.x += self.speed_x
        self.y += self.speed_y

        return self.x, self.y

class Game:
    def __init__(self):
        self.freeze_time = 60
        self.score_p = 1
        self.fps_timer = time.time()  # Инициализируем таймер

    def show_game_over_message(self, score):
        root = tk.Tk()
        root.title("Игра окончена")
        root.withdraw()

        def play_again():
            root.destroy()
            self.main()

        def close_game():
            root.destroy()

        # Увеличиваем размер окна
        root.geometry("300x150")

        message = tk.Label(root, text=f"Вы проиграли. Ваши очки: {score}")
        message.pack()

        play_again_button = tk.Button(root, text="Играть заново", command=play_again)
        play_again_button.pack()

        close_button = tk.Button(root, text="Ок", command=close_game)
        close_button.pack()

        root.deiconify()
        root.mainloop()

    def select_difficulty(self):
        root = tk.Tk()
        root.title("Выбор сложности")

        def set_difficulty(difficulty):
            if difficulty == "Легкий":
                self.freeze_time, self.score_p = 60, 1
            elif difficulty == "Средний":
                self.freeze_time, self.score_p = 120, 5
            elif difficulty == "Сложный":
                self.freeze_time, self.score_p = 240, 10
            root.destroy()

        tk.Label(root, text="Выберите уровень сложности:").pack()
        tk.Button(root, text="Легкий", command=lambda: set_difficulty("Легкий")).pack()
        tk.Button(root, text="Средний", command=lambda: set_difficulty("Средний")).pack()
        tk.Button(root, text="Сложный", command=lambda: set_difficulty("Сложный")).pack()

        root.mainloop()

    def main(self):
        self.select_difficulty()
        pyray.set_target_fps(self.freeze_time)
        width = 800
        height = 600
        pyray.init_window(width, height, "Мяч с платформой")

        ball = Ball(width, height)

        platform_x = width // 2
        platform_y = height - 70
        platform_width = 100
        platform_speed = 3

        game_over = False
        score = 0
        last_hit_platform = False

        while not pyray.window_should_close() and not game_over:
            pyray.begin_drawing()

            pyray.clear_background(colors.BLACK)

            if pyray.is_key_down(pyray.KEY_A) and platform_x - platform_speed >= 0:
                platform_x -= platform_speed
            if pyray.is_key_down(pyray.KEY_D) and platform_x + platform_width + platform_speed <= width:
                platform_x += platform_speed

            pyray.draw_rectangle(platform_x, platform_y, platform_width, 10, colors.BLUE)

            # Обновляем показатель FPS каждые 3 секунды
            current_time = time.time()
            if current_time - self.fps_timer >= 3:
                self.fps_timer = current_time
                self.freeze_time += 2
                pyray.set_target_fps(self.freeze_time)

            ball_x, ball_y = ball.update(width, height)
            pyray.draw_texture(ball.texture, ball_x - ball.texture.width // 2, ball_y - ball.texture.height // 2, colors.WHITE)

            if ball_y + 50 >= platform_y and ball_x >= platform_x and ball_x <= platform_x + platform_width and ball_y <= platform_y:
                if not last_hit_platform:
                    ball.speed_y = -ball.speed_y
                    score += self.score_p
                    last_hit_platform = True
            else:
                last_hit_platform = False

            if ball_y + 50 > height:
                game_over = True

            pyray.draw_text(f"Score: {score}", 10, 10, 20, colors.WHITE)

            pyray.end_drawing()

        pyray.close_window()
        self.show_game_over_message(score)

if __name__ == '__main__':
    game = Game()
    game.main()
