from pygame import *
import random
import time as pytime
mixer.init()

WIDTH, HEIGHT = 1920, 1080
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Космический шутер")

clock = time.Clock()
FPS = 144

background = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))

mixer.music.load("space.ogg")
mixer.music.play(-2)
fire_sound = mixer.Sound("fire.ogg")

font.init()
stats_font = font.Font(None, 36)
large_font = font.Font(None, 72)

class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, width, height, speed=0):
        super().__init__()
        self.image = transform.scale(image.load(image_file), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            global missed_enemies
            missed_enemies += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH - self.rect.width)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player("rocket.png", WIDTH // 2 - 25, HEIGHT - 80, 50, 80, 5)

enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("ufo.png", random.randint(0, WIDTH - 50), -100, 50, 50, 1.3)
    enemies.add(enemy)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("asteroid.png", random.randint(0, WIDTH - 50), -100, 60, 60, 1.0)
    asteroids.add(asteroid)

bullets = sprite.Group()

missed_enemies = 0
destroyed_enemies = 0
lives = 3
score = 0
game_over = False

running = True
result_message = ""

while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE and not game_over:
                bullet = Bullet("bullet.png", player.rect.centerx - 5, player.rect.top, 10, 20, 10)
                bullets.add(bullet)
                fire_sound.play()  
    
    if not game_over:
        player.update()
        enemies.update()
        asteroids.update()
        bullets.update()

        hits = sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            destroyed_enemies += 1
            score += 100
            enemy = Enemy("ufo.png", random.randint(0, WIDTH - 50), -100, 50, 50, 2)
            enemies.add(enemy)
        
        asteroid_hits = sprite.groupcollide(bullets, asteroids, True, False)
        
        if sprite.spritecollide(player, enemies, True) or sprite.spritecollide(player, asteroids, False):
            lives -= 1
            enemy = Enemy("ufo.png", random.randint(0, WIDTH - 50), -100, 50, 50, 2)
            enemies.add(enemy)
        
        if lives <= 0:
            result_message = "YOU LOSE!"
            game_over = True
        elif missed_enemies >= 10:
            result_message = "YOU LOSE!"
            game_over = True
        elif score >= 1000:
            result_message = "YOU WIN!"
            game_over = True
    
    screen.blit(background, (0, 0))
    
    missed_text = stats_font.render(f"Пропущено: {missed_enemies}", True, (255, 255, 255))
    destroyed_text = stats_font.render(f"Сбито: {destroyed_enemies}", True, (255, 255, 255))
    score_text = stats_font.render(f"Очки: {score}", True, (255, 255, 255))
    lives_text = stats_font.render(f"Жизни: {lives}", True, (255, 255, 255))
    
    screen.blit(missed_text, (10, 10))
    screen.blit(destroyed_text, (10, 50))
    screen.blit(score_text, (10, 90))
    screen.blit(lives_text, (10, 130))
    
    player.draw(screen)
    enemies.draw(screen)
    asteroids.draw(screen)
    bullets.draw(screen)
    
    if game_over:
        result_text = large_font.render(result_message, True, (255, 255, 255))
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, HEIGHT//2))
        
        if lives <= 0:
            reason_text = stats_font.render("Вы потеряли все жизни!", True, (255, 255, 255))
        elif missed_enemies >= 10:
            reason_text = stats_font.render("Пропущено слишком много врагов!", True, (255, 255, 255))
        else:
            reason_text = stats_font.render("Вы набрали 1000 очков!", True, (255, 255, 255))
        
        screen.blit(reason_text, (WIDTH//2 - reason_text.get_width()//2, HEIGHT//2 + 80))
    
    display.flip()
    clock.tick(FPS)

if result_message:
    print(result_message)
    pytime.wait(3000)