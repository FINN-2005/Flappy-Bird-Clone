from mine.pygame_template import *
from os.path import join



# GAME DIFFICULTY (just uncomment the ones you don't want)

# difficulty = 150, 170       # impossible
# difficulty = 150, 190       # Hard
# difficulty = 160, 220       # mid
difficulty = 170, 270       # easy




APP.H = 800
APP.W = APP.H * 0.5625

scale_factor = 1.5625

def load_surfaces() -> dict:
    surfs = dict()

    surfs['bird_up'] = pygame.transform.scale_by(pygame.image.load(join('images', 'bird_up.png')).convert_alpha(), scale_factor)
    surfs['bird_mid'] = pygame.transform.scale_by(pygame.image.load(join('images', 'bird_mid.png')).convert_alpha(), scale_factor)
    surfs['bird_down'] = pygame.transform.scale_by(pygame.image.load(join('images', 'bird_down.png')).convert_alpha(), scale_factor)

    surfs['pipe'] = pygame.transform.scale_by(pygame.image.load(join('images', 'pipe.png')).convert_alpha(), scale_factor)

    surfs['bg'] = pygame.transform.scale_by(pygame.image.load(join('images', 'bg.png')).convert_alpha(), scale_factor)
    surfs['ground'] = pygame.transform.scale_by(pygame.image.load(join('images', 'ground.png')).convert_alpha(), scale_factor)

    surfs['game_over'] = pygame.transform.scale_by(pygame.image.load(join('text', 'gameover.png')).convert_alpha(), scale_factor)
    surfs['start_screen'] = pygame.transform.scale_by(pygame.image.load(join('text', 'message.png')).convert_alpha(), scale_factor)

    for i in range(10):
        surfs[i] = pygame.transform.scale_by(pygame.image.load(join('text', 'numbers', f'{i}.png')).convert_alpha(), scale_factor)

    return surfs

def load_sounds():
    sounds = {
        'die': pygame.mixer.Sound('sounds/die.wav'),
        'hit': pygame.mixer.Sound('sounds/hit.wav'),
        'point': pygame.mixer.Sound('sounds/point.wav'),
        'swoosh': pygame.mixer.Sound('sounds/swoosh.wav'),
        'wing': pygame.mixer.Sound('sounds/wing.wav'),
    }

    sounds['die'].set_volume(0.07 + 0.5)
    sounds['hit'].set_volume(0.04 + 0.5)
    sounds['point'].set_volume(0.2 + 0.5)
    sounds['swoosh'].set_volume(0.1 + 0.5)
    sounds['wing'].set_volume(0.1 + 0.5)

    return sounds

