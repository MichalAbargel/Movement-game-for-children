import pygame

pygame.mixer.init()


def play_well_done():
    pygame.mixer.music.load("win-2-short.mp3")
    if not pygame.mixer.music.get_busy():
        print("play win")
        pygame.mixer.music.play()
    else:
        print("player is busy")


def play_try_again():
    # sound = pygame.mixer.Sound("\opps.mp3")
    pygame.mixer.music.load("opps.mp3")
    if not pygame.mixer.music.get_busy():
        print("play lose")
        pygame.mixer.music.play()
    else:
        print("player is busy")


def is_busy():
    return pygame.mixer.music.get_busy()