from settings import *
from classes import Bird, Pipe, StaticSprite

class run(APP):

    def init(self):
        self.dt_speed_factor = 10
    
    def setup(self):
        self.surfs = load_surfaces()
        self.sounds = load_sounds()
        self.game_over = False
        self.has_started = False
        self.score = 0
        self.scroll_speed = [15]
        self.scored_pipes = []
        self.played_die = False
        self.make_faster = False
        self.group = Group()

        self.bg_layer = Group()
        self.pipe_layer = Group()
        self.ground_layer = Group()
        self.bird_layer = Group()

        StaticSprite(self.surfs['bg'], (0, 0), self.group, self.bg_layer)

        ground_y = APP.H - self.surfs['ground'].get_height()
        StaticSprite(self.surfs['ground'], (0, ground_y), self.group, self.ground_layer)

        bird_surfaces = [self.surfs['bird_up'], self.surfs['bird_mid'], self.surfs['bird_down'], self.surfs['bird_mid']]
        self.bird = Bird(bird_surfaces, self.sounds, self.group, self.bird_layer)

        self.pipe_spacing = APP.W * 0.5
        self.pipe_timer = 0
        self.pipe_interval = self.pipe_spacing / 10
        Pipe(self.scroll_speed, self.surfs['pipe'], APP.W * 1.2, self.group, self.pipe_layer)

    def check_collision(self):
        pipe_hit = pygame.sprite.spritecollide(self.bird, self.pipe_layer, False, pygame.sprite.collide_mask)
        ground_hit = self.bird.rect.bottom >= APP.H - self.surfs['ground'].get_height()
        ceiling_hit = self.bird.rect.top <= 0
        return pipe_hit or ground_hit or ceiling_hit

    def update(self):
        global SCROLL_SPEED
        dt = self.dt

        print(self.make_faster, self.scroll_speed)
        if self.has_started:
            if not self.game_over:
                self.pipe_timer += dt
                if self.pipe_timer >= self.pipe_interval:
                    self.pipe_timer = 0
                    Pipe(self.scroll_speed, self.surfs['pipe'], APP.W + 100, self.group, self.pipe_layer)

                self.group.update(dt)

                if self.check_collision():
                    self.sounds['hit'].play()
                    self.sounds['die'].play()
                    self.game_over = True

                for sprite in self.pipe_layer:
                    if sprite.rect.right < self.bird.rect.centerx and sprite not in self.scored_pipes:
                        self.score += 1
                        if self.score % 5 == 0: self.make_faster = True
                        self.scored_pipes.append(sprite)
                        self.sounds['point'].play()
                    if sprite.rect.right < 0:
                        sprite.kill()
                if self.make_faster:
                    self.scroll_speed[0] += 1.5
                    self.make_faster = False
                
            else:
                self.bird.update(dt)

                bird_bottom = self.bird.rect.bottom
                ground_top = APP.H - self.surfs['ground'].get_height()

                if bird_bottom >= ground_top:
                    self.bird.velocity.y = 0
                    self.bird.rect.bottom = ground_top

                pipe_hit = pygame.sprite.spritecollide(self.bird, self.pipe_layer, False, pygame.sprite.collide_mask)
                if pipe_hit: self.bird.velocity.y = 0

                if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                    self.sounds['swoosh'].play()
                    self.setup()
        else:
            if pygame.key.get_just_pressed()[pygame.K_SPACE]:
                self.sounds['swoosh'].play()
                self.has_started = True
    
    def draw(self):
        if self.has_started:
            self.bg_layer.draw()
            self.pipe_layer.draw()
            self.ground_layer.draw()
            self.bird_layer.draw()
            if self.game_over:
                img = self.surfs['game_over']
                rect = img.get_frect(center=V2(APP.HW, APP.H * 0.25))
                self.group.screen.blit(img, rect)
                
                score_str = str(self.score)
                digits = [pygame.transform.scale_by(self.surfs[int(d)], 1.5) for d in score_str]
                total_width = sum(d.get_width() for d in digits)
                x = APP.HW - total_width // 2
                y = APP.HH                
                for digit in digits:
                    rect = digit.get_frect(topleft=(x, y))
                    self.group.screen.blit(digit, rect)
                    x += digit.get_width()
            else: 
                score_str = str(self.score)
                digits = [self.surfs[int(d)] for d in score_str]

                total_width = sum(d.get_width() for d in digits)
                x = APP.HW - total_width // 2
                y = APP.H * 0.1

                for digit in digits:
                    rect = digit.get_frect(topleft=(x, y))
                    self.group.screen.blit(digit, rect)
                    x += digit.get_width()
        else:
            self.bg_layer.draw()
            self.ground_layer.draw()
            img = self.surfs['start_screen']
            rect = img.get_frect(center = V2(APP.HW,APP.HH))
            self.group.screen.blit(img, rect)


run()