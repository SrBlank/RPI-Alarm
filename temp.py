import pygame
import time

pygame.init()

pygame.mixer.music.load("./src/alarm_sounds/generic_alarm.mp3")
pygame.mixer.music.set_volume(.9)
pygame.mixer.music.play()

time.sleep(3)

pygame.mixer.music.stop()