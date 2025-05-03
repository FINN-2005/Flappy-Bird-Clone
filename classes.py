from settings import *

class Bird(Sprite):
    def __init__(self, surf_list: list[pygame.Surface], sounds, *groups):
        super().__init__(*groups)

        self.frames = surf_list
        self.sounds = sounds  # <- added
        self.frame_index = 0
        self.animation_speed = 1.5
        self.frame_timer = 0

        self.original_image = self.frames[0].copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_frect(center=V2(APP.HW * 0.5, APP.HH * 0.3))
        self.mask = pygame.mask.from_surface(self.image)

        self.velocity = V2()
        self.gravity = 8
        self.jump_force = -35

    def update(self, dt):
        key = pygame.key.get_just_pressed()[pygame.K_SPACE]
        if key:
            self.velocity.y = self.jump_force
            self.sounds['wing'].play()  # <- added

        self.velocity.y += self.gravity * dt
        self.rect.topleft = V2(self.rect.topleft) + self.velocity * dt

        self.frame_timer += dt * self.animation_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.original_image = self.frames[self.frame_index]

        angle = max(-50, min(50, -self.velocity.y * 2))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_frect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)



class Pipe(Sprite):
    def __init__(self, scroll_speed, surf:pygame.Surface, x, *groups):
        super().__init__(*groups)

        self.scroll_speed = scroll_speed

        self.pipe_surf = surf.copy()
        self.pipe_rect = self.pipe_surf.get_frect()

        self.inverted_pipe_surf = pygame.transform.flip(self.pipe_surf, False, True)
        self.inverted_pipe_rect = self.inverted_pipe_surf.get_frect()

        grace = difficulty[0]
        self.opening = random.randint(0 + grace, APP.H - grace - 112)
        self.opening_width = random.randint(*difficulty)
        
        self.image = pygame.Surface((self.pipe_surf.width, APP.H), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_frect(left=x)
        
        self.pipe_rect.top = self.opening + self.opening_width / 2
        self.inverted_pipe_rect.bottom = self.opening - self.opening_width / 2

        self.image.blit(self.pipe_surf, self.pipe_rect)
        self.image.blit(self.inverted_pipe_surf, self.inverted_pipe_rect)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.x -= self.scroll_speed[0] * dt



class StaticSprite(Sprite):
    def __init__(self, surf: pygame.Surface, pos=(0, 0), *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)

