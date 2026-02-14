from tkinter import *
import time
import random

class Ball:
    def __init__(self, canvas, platform, color):
        self.canvas = canvas
        self.platform = platform
        self.oval = self.canvas.create_oval(200, 200, 215, 215, fill=color)

        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -3

        self.touch_bottom = False

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        return (
            ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]
            and ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]
        )

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        ball_pos = self.canvas.coords(self.oval)

    
        if ball_pos[0] <= 0:
            self.x = abs(self.x)
        if ball_pos[2] >= self.canvas.winfo_width():
            self.x = -abs(self.x)

        
        if ball_pos[1] <= 0:
            self.y = abs(self.y)

        
        if ball_pos[3] >= self.canvas.winfo_height():
            self.touch_bottom = True

        
        if self.touch_platform(ball_pos):
            self.y = -abs(self.y)


class Platform:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = self.canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.rect, 200, 330)

    def move_left(self, event=None):
        self.canvas.move(self.rect, -20, 0)
        self._clamp()

    def move_right(self, event=None):
        self.canvas.move(self.rect, 20, 0)
        self._clamp()

    def _clamp(self):
        pos = self.canvas.coords(self.rect)
        if pos[0] < 0:
            self.canvas.move(self.rect, -pos[0], 0)
        if pos[2] > self.canvas.winfo_width():
            self.canvas.move(self.rect, self.canvas.winfo_width() - pos[2], 0)



window = Tk()
window.title("Ball Game")
window.resizable(False, False)

canvas = Canvas(window, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()


window.update_idletasks()
window.update()

platform = Platform(canvas, "blue")
ball = Ball(canvas, platform, "red")


window.bind("<Left>", platform.move_left)
window.bind("<Right>", platform.move_right)

def game_loop():
    if not ball.touch_bottom:
        ball.draw()
        window.after(10, game_loop)
    else:
        canvas.create_text(250, 200, text="GAME OVER", font=("Arial", 24), fill="black")

game_loop()
window.mainloop()