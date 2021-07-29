from board_classes import *

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

chessboard = Game_Board(screen)
is_running = True

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            chessboard.btn_down(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            chessboard.btn_up(event.pos)

        if event.type == pygame.MOUSEMOTION:
            chessboard.drag(event.pos)
    clock.tick(FPS)

pygame.quit()
