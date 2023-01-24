import pygame

pygame.mixer.init()


def play_well_done():
    pygame.mixer.music.load("media/win-2-short.mp3")
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()


def play_try_again():
    # sound = pygame.mixer.Sound("\opps.mp3")
    pygame.mixer.music.load("media/opps.mp3")
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()


def is_busy():
    return pygame.mixer.music.get_busy()


def play_click():
    pygame.mixer.music.load("media/click.mp3")
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
