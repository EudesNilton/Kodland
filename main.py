import pgzrun
import random
from pygame import Rect

WIDTH = 800
HEIGHT = 600

ship_idle = "ship"
ship_right = ["shipr1", "shipr2", "shipr3"]
ship_left = ["shipl1", "shipl2", "shipl3"]
alien_frames = ["alien1", "alien2", "alien3"]

class Ship(Actor):
    def __init__(self, x, y):
        super().__init__("ship", (x, y))
        self.scale = 0.25
        self.current_frame = 0
        self.current_direction = "idle"
        self.last_direction = "idle"
        self.frame_timer = 0  

    def update_sprite(self):
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame_timer = 0 
            if self.current_direction == "right":
                self.image = ship_right[self.current_frame % len(ship_right)]
            elif self.current_direction == "left":
                self.image = ship_left[self.current_frame % len(ship_left)]
            else:
                self.image = ship_idle

            if self.current_direction != self.last_direction:
                self.current_frame = 0
            self.last_direction = self.current_direction

            self.current_frame += 1


    def move_left(self):
        if self.x > 50:
            self.x -= 4
            self.current_direction = "left"

    def move_right(self):
        if self.x < WIDTH - 50:
            self.x += 4
            self.current_direction = "right"

    def stop(self):
        if self.current_direction != "idle":
            self.current_direction = "idle"

class Alien(Actor):
    def __init__(self, x, y):
        super().__init__(alien_frames[0], (x, y))
        self.scale = 0.25
        self.frame = 0
        self.frame_timer = 0 

    def update_sprite(self):
        self.frame_timer += 1
        if self.frame_timer >= 10:
            self.frame_timer = 0 
            self.image = alien_frames[self.frame % len(alien_frames)]
            self.frame += 1


class Bullet(Actor):
    def __init__(self, x, y):
        super().__init__('bullet', (x, y))
    
    def move(self):
        self.y -= 5

ship = Ship(WIDTH // 2, HEIGHT - 50)
bullets = []
aliens = []
score = 0
running = False
menu = True
sound_on = True

def spawn_alien():
    if running:
        x = random.randint(50, WIDTH - 50)
        alien = Alien(x, 50)
        aliens.append(alien)

def play_background_music():
    if sound_on:
        sounds.bgsong.play(-1)

play_background_music()

def update():
    global score, running, menu

    if not running:
        return
    
    if keyboard.left:
        ship.move_left()
    elif keyboard.right:
        ship.move_right()
    else:
        ship.stop()

    ship.update_sprite()

    for bullet in bullets[:]:
        bullet.move()
        if bullet.y < 0:
            bullets.remove(bullet)
    
    for alien in aliens[:]:
        alien.y += 2
        alien.update_sprite()

        if alien.y > HEIGHT:
            running = False
            menu = False
        
        if Rect(alien.left, alien.top, alien.width, alien.height).colliderect(
           Rect(ship.left, ship.top, ship.width, ship.height)):
            running = False
            menu = False

        for bullet in bullets[:]:
            if Rect(alien.left, alien.top, alien.width, alien.height).colliderect(
               Rect(bullet.left, bullet.top, bullet.width, bullet.height)):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 10
                break

def draw():
    screen.clear()

    if menu:
        screen.draw.text("Space Shooter", center=(WIDTH//2, HEIGHT//4), fontsize=60, color='white')
        screen.draw.text("Press ENTER to Start", center=(WIDTH//2, HEIGHT//2), fontsize=40, color='yellow')
        screen.draw.text("Press S to Toggle Sound", center=(WIDTH//2, HEIGHT//2 + 50), fontsize=30, color='gray')
        sound_text = "Sound On" if sound_on else "Sound Off"
        screen.draw.text(sound_text, center=(WIDTH//2, HEIGHT//2 + 100), fontsize=30, color='white')
        screen.draw.text("Press ESC to Exit", center=(WIDTH//2, HEIGHT//2 + 200), fontsize=30, color='red')
    elif running:
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for alien in aliens:
            alien.draw()
        screen.draw.text(f'Score: {score}', (10, 10), color='white')
    else:
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), fontsize=60, color='red')
        screen.draw.text(f'Final Score: {score}', center=(WIDTH//2, HEIGHT//2 + 40), fontsize=40, color='white')
        screen.draw.text("Press R to Restart", center=(WIDTH//2, HEIGHT//2 + 80), fontsize=30, color='green')
        screen.draw.text("Press ESC to Exit", center=(WIDTH//2, HEIGHT//2 + 150), fontsize=30, color='red')

def on_key_down(key):
    global running, menu, bullets, aliens, score, sound_on

    if menu:
        if key == keys.RETURN:
            running = True
            menu = False
        elif key == keys.S:
            sound_on = not sound_on
            if sound_on:
                sounds.bgsong.play(-1)
            else:
                sounds.bgsong.stop()
    elif key == keys.ESCAPE:
        exit()
    elif not running:
        if key == keys.R:
            running = True
            menu = False
            bullets = []
            aliens = []
            score = 0
            ship.pos = (WIDTH // 2, HEIGHT - 50)
    else:
        if key == keys.SPACE:
            bullet = Bullet(ship.x, ship.y - 20)
            sounds.laser.play()
            bullets.append(bullet)

clock.schedule_interval(spawn_alien, 1.3)
clock.schedule_interval(lambda: [alien.update_sprite() for alien in aliens], 0.2)
clock.schedule_interval(ship.update_sprite, 0.2)

pgzrun.go()
