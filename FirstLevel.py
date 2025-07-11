import pygame
from pygame.locals import *
from Eva import Eva
from Angel import Angel
import pygame.mixer

class FirstLevel:
    def __init__(self, window):
        self.window = window
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        info = pygame.display.Info()
        self.WIDTH, self.HEIGHT = info.current_w, info.current_h
        
        # Шрифты (полностью идентичные другим уровням)
        self.menu_font = pygame.font.Font('static/fonts/main_font.otf', 20)
        self.font1 = pygame.font.Font('static/fonts/main_font.otf', 54)
        self.font2 = pygame.font.Font('static/fonts/main_font.otf', 55)
        self.font_main = pygame.font.Font('static/fonts/main_font.otf', 70)
        
        # Кнопка меню (в том же стиле и положении)
        self.menu_text = self.menu_font.render('Menu', True, 'white')
        self.menu_rect = self.menu_text.get_rect(bottomright=(140, self.HEIGHT - 30))
        
        # Таймер для анимации текста (как в других уровнях)
        self.timer = 0
        self.active = False
        
        # Загрузка ресурсов
        try:
            self.imgBG = pygame.image.load('static/photo/game_background.png').convert()
            self.imgBG = pygame.transform.scale(self.imgBG, (self.WIDTH, self.HEIGHT))
            self.imgEva = pygame.image.load('static/photo/eva_01.png').convert_alpha()
            self.imgEva = pygame.transform.scale(self.imgEva, (200, 350))
            self.imgAngel = pygame.image.load('static/photo/angel_endgame.png').convert_alpha()
            self.imgAngel = pygame.transform.scale(self.imgAngel, (150, 150))
            self.imgLaser = pygame.image.load('static/photo/laser.png').convert_alpha()
            self.imgLaser = pygame.transform.scale(self.imgLaser, (60, 20))
            
            # Звуки (те же что в других уровнях)
            self.congratulations = pygame.mixer.Sound('static/music/congratulations.wav')
            self.lose_sound = pygame.mixer.Sound('static/music/lose.wav')
        except pygame.error as e:
            print(f"Ошибка загрузки ресурсов: {e}")
            self.imgBG = pygame.Surface((self.WIDTH, self.HEIGHT))
            self.imgBG.fill((50, 50, 100))
            # Заглушки для звуков
            self.congratulations = None
            self.lose_sound = None
        
        self.reset_level_state()

    def reset_level_state(self):
        """Полный сброс состояния уровня"""
        self.eva_bullets = []
        self.angel_bullets = []
        self.eva_health = 3
        self.angel_health = 20
        self.last_shot_time_eva = 0
        self.DEBUG_MODE = False
        self.running = True
        self.active = False
        self.is_music_playing = False
        self.game_end = False
        self.is_win = False
        self.is_click = True
        self.timer = 0

        # Переинициализация персонажей
        self.eva = Eva(
            window=self.window,
            evaPX=30,
            evaPY=self.HEIGHT//2,
            width=200,
            height=250,
            img=self.imgEva,
            width_s=self.WIDTH,
            height_s=self.HEIGHT,
            eva_bullets=self.eva_bullets,
            bullet_img=self.imgLaser
        )
        self.angel = Angel(
            window=self.window,
            x=self.WIDTH-30,
            y=self.HEIGHT//2,
            screen_width=self.WIDTH,
            screen_height=self.HEIGHT,
            angel_bullets=self.angel_bullets,
            bullet_img=self.imgLaser,
            angel_img=self.imgAngel
        )

    def update_bullets(self):
        # Обновление пуль (без изменений)
        for bullet in self.eva_bullets[:]:
            bullet.update()
            if bullet.px > self.WIDTH or self.check_angel_hit(bullet):
                self.eva_bullets.remove(bullet)
                if bullet.px <= self.WIDTH:
                    self.angel_health -= 1

        for bullet in self.angel_bullets[:]:
            bullet.update(self.WIDTH)
            if not bullet.active or self.check_eva_hit(bullet):
                self.angel_bullets.remove(bullet)
                if not bullet.active:
                    continue
                self.eva_health -= 1

    def update(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        if not self.active:
            return
                
        # Управление Евой
        self.eva.eva_move(keys)
        
        # Стрельба
        if keys[K_SPACE] and current_time - self.last_shot_time_eva > 500:
            self.eva.shooting(current_time)
            self.last_shot_time_eva = current_time
        
        # Обновление Ангела
        self.angel.update(current_time)
        self.update_bullets()
        
        # Проверка условий завершения уровня
        if self.eva_health <= 0 or self.angel_health <= 0:
            self.handle_level_end(self.angel_health <= 0)

    def handle_level_end(self, is_win):
        """Обработка завершения уровня"""
        self.running = False
        self.is_win = is_win
        self.game_end = True
        
        if not self.is_music_playing:
            if is_win and self.congratulations:
                self.congratulations.play()
            elif not is_win and self.lose_sound:
                self.lose_sound.play()
            self.is_music_playing = True

    def draw_health_bars(self):
        # Полосы здоровья (без изменений)
        pygame.draw.rect(self.window, (255, 0, 0), (20, 20, 200, 20))
        pygame.draw.rect(self.window, (0, 255, 0), (20, 20, 200 * (self.eva_health / 3), 20))
        pygame.draw.rect(self.window, (255, 0, 0), (self.WIDTH - 220, 20, 200, 20))
        pygame.draw.rect(self.window, (0, 255, 0), (self.WIDTH - 220, 20, 200 * (self.angel_health / 20), 20))

    def check_collision(self, bullet, target_rect):
        return target_rect.colliderect(bullet.get_rect())

    def check_eva_hit(self, bullet):
        eva_rect = pygame.Rect(self.eva.px + 40, self.eva.py + 30, 120, 190)
        return self.check_collision(bullet, eva_rect)

    def check_angel_hit(self, bullet):
        angel_rect = pygame.Rect(
            self.angel.x - self.angel.img_width//2,
            self.angel.y,
            self.angel.img_width,
            self.angel.img_height
        )
        return self.check_collision(bullet, angel_rect)

    def draw(self):
        # Отрисовка фона
        self.window.blit(self.imgBG, (0, 0))
        
        if not self.active:
            # Экран начала уровня (как в других уровнях)
            self.timer = (self.timer + 1) % 60
            if self.timer % 30 < 15:
                start_text = self.font2.render('Press any key to start...', True, 'white')
            else:
                start_text = self.font1.render('Press any key to start...', True, 'white')
            
            start_text_rect = start_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 100))
            self.window.blit(start_text, start_text_rect)
            
            title_text = self.font2.render('First Level', True, 'white')
            title_rect = title_text.get_rect(center=(self.WIDTH // 2, 100))
            self.window.blit(title_text, title_rect)
        else:
            # Основная игровая отрисовка
            self.eva.draw_eva()
            self.angel.draw()
            
            for bullet in self.eva_bullets:
                bullet.draw(self.window)
            for bullet in self.angel_bullets:
                bullet.draw(self.window)
            
            self.draw_health_bars()
        
        # Кнопка меню (всегда отображается)
        self.window.blit(self.menu_text, self.menu_rect)
        mouse_pos = pygame.mouse.get_pos()
        if self.menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.window, pygame.Color('white'), self.menu_rect.inflate(10, 10), 3, 5)

    def event_handler(self, event):
        if event.type == pygame.QUIT:
            self.running = False
            return "exit"
        
        if not self.active:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:  # Любая клавиша или клик мыши
                mouse_pos = pygame.mouse.get_pos()
                if self.menu_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                    return "menu"
                else:
                    self.active = True
                    return None
            
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            if event.key == K_d:
                self.DEBUG_MODE = not self.DEBUG_MODE
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.menu_rect.collidepoint(mouse_pos):
                return "menu"
            
        return None

    def end_window(self):
        """Экран завершения уровня (без изменений)"""
        to_return = None
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        overlay = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.window.blit(overlay, (0, 0))

        if self.is_win:
            title = self.font_main.render('Level Complete!', True, 'white')
            title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
            self.window.blit(title, title_rect)

            continue_text = self.font1.render('Continue', True, 'white')
            continue_rect = continue_text.get_rect(center=(self.WIDTH//2 + 200, self.HEIGHT//3 + 470))
            self.window.blit(continue_text, continue_rect)
            
            again_text = self.font1.render('Try Again', True, 'white')
            again_rect = again_text.get_rect(center=(self.WIDTH//2 - 200, self.HEIGHT//3 + 470))
            self.window.blit(again_text, again_rect)
            
            if continue_rect.collidepoint(mouse_pos) and mouse_clicked and self.is_click:
                to_return = 'continue'
            elif again_rect.collidepoint(mouse_pos) and mouse_clicked and self.is_click:
                to_return = 'again'
        else:
            title = self.font_main.render('Mission Failed', True, 'white')
            title_rect = title.get_rect(center=(self.WIDTH//2, self.HEIGHT//3))
            self.window.blit(title, title_rect)

            again_text = self.font1.render('Try Again', True, 'white')
            again_rect = again_text.get_rect(center=(self.WIDTH//2, self.HEIGHT//3 + 470))
            self.window.blit(again_text, again_rect)
            
            if again_rect.collidepoint(mouse_pos) and mouse_clicked and self.is_click:
                to_return = 'again'

        self.window.blit(self.menu_text, self.menu_rect)
        if self.menu_rect.collidepoint(mouse_pos) and mouse_clicked and self.is_click:
            to_return = 'menu'

        if mouse_clicked:
            self.is_click = False
        else:
            self.is_click = True

        return to_return

    def run(self):
        """Основной игровой цикл"""
        for event in pygame.event.get():
            result = self.event_handler(event)
            if result == "menu":
                self.reset_level_state()
                return "menu"
            elif result == "exit":
                return "exit"
        
        if self.game_end:
            next_step = self.end_window()
            if next_step == "continue":
                return "continue"
            elif next_step == "again":
                self.reset_level_state()
                return None
            elif next_step == "menu":
                self.reset_level_state()
                return "menu"
            return None
        
        # Проверка нажатия кнопки меню во время игры
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        if self.menu_rect.collidepoint(mouse_pos) and mouse_clicked and self.is_click:
            if not self.active or self.active:  # Работает в любом состоянии
                self.reset_level_state()
                return "menu"
        
        self.update()
        self.draw()
        
        return None