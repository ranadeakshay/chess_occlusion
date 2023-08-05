import pygame
pygame.init()
screen = pygame.display.set_mode((128, 128))
clock = pygame.time.Clock()

counter, text = 10, '10'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Consolas', 30)

while True:
    for e in pygame.event.get():
        if e.type == pygame.USEREVENT:
            print(e)
            counter -= 1
            text = str(counter).rjust(3) if counter > 0 else 'boom!'
        if e.type == pygame.QUIT: break
    else:
        screen.fill((255, 255, 255))
        screen.blit(font.render(text, True, (0, 0, 0)), (32, 48))
        pygame.display.flip()
        clock.tick(60)
        continue
    break




# import pygame as p
#
# p.init()
#
# timer_left = 999
# timer_update = timer_left
# start_time = p.time.get_ticks()
#
# while True:
#     time_elapsed = (p.time.get_ticks() - start_time) // 1000
#     timer_update -= time_elapsed
#
#     print(time_elapsed)