import pygame
import sys
import time
import tictactoe as ttt
import random_ai
from mcts import best_move



pygame.init()
pygame.display.set_caption("Ultimate TicTacToe")
size = width, height = 800, 750
center = width/2, height/2+20
tile_size = height/15

screen = pygame.display.set_mode(size)

large_font = pygame.font.Font("OpenSans-Regular.ttf", 60)
medium_font = pygame.font.Font("OpenSans-Regular.ttf", 28)
move_font = pygame.font.Font("OpenSans-Regular.ttf", 40)


home_page = True #if display home page or not
play_vs_ai = False # if user wants to play against AI or not
game_over = False
user = None


state = ttt.initial_state()


def display_board():

    global game_over, player, home_page, play_vs_ai, state, tiles


    board = state[0]
    valid_action = state[1]
    
    if valid_action!=0:
        R_valid, C_valid = valid_action
    else:
        R_valid, C_valid = -1, -1

    tiles = []

    for R in range(3):
        Row = []
        for C in range(3):
            Column = []
            for r in range(3):
                row = []
                for c in range(3):
                    rect = pygame.Rect(
                        center[0] + (C*3+c-4)*tile_size,
                        center[1] + (R*3+r-4)*tile_size,
                        tile_size, tile_size
                    )
                    rect.center = center[0] + (C*3+c-4)*tile_size,center[1] + (R*3+r-4)*tile_size

                    if (R==R_valid and C==C_valid):
                        pygame.draw.rect(screen, 'yellow', rect, 3)
                    elif C_valid == -1 and not ttt.mini_board_terminal(board[R, C]):
                        pygame.draw.rect(screen, 'yellow', rect, 3)
                    else:
                        pygame.draw.rect(screen, 'white', rect, 3)
                    

                    if board[R, C, r, c] != ttt.EMPTY:
                        colour = 'red' if board[R, C, r, c]==ttt.X else 'blue'
                        move = move_font.render(board[R, C, r, c], True, colour)
                        moveRect = move.get_rect()
                        moveRect.center = rect.center
                        screen.blit(move, moveRect)
                    row.append(rect)
                Column.append(row)
            Row.append(Column)
        tiles.append(Row)
    
    for R in range(3):
        for C in range(3):
            rect = pygame.Rect(
                0, 0,
                3*tile_size, 3*tile_size
            )
            
            
            rect.center = center[0] + (C-1)*tile_size*3, center[1] + (R-1)*tile_size*3

            pygame.draw.rect(screen, 'black', rect, 10)
            pygame.draw.rect(screen, 'white', rect, 1)

    game_over = ttt.terminal(state)
    player = ttt.player(state)

    #if game is over
    if game_over:
        winner = ttt.winner(state)
        if winner is None:
            title = f"Game Over: Tie"
        else:
            title = f"Game Over: {winner} wins"
    elif not play_vs_ai:
        title = f"Play as {player}"
    else:
        if player==user:
            title = f"Play as {player}"
        else:
            title = "Computer thinking..."
    
    title = large_font.render(title, True, 'white')
    titleRect = title.get_rect()
    titleRect.center = (width/2, 50)
    screen.blit(title, titleRect)    

    if game_over:
        
        againButton = pygame.Rect(0, 0, width/4, 50)
        againButton.center = width/2, height-50
        again = medium_font.render("Play Again", True, 'black')
        againRect = again.get_rect()
        againRect.center = againButton.center
        pygame.draw.rect(screen, 'white', againButton)
        screen.blit(again, againRect)

        click, _, _ = pygame.mouse.get_pressed()

        if click == 1:
            mouse_pos = pygame.mouse.get_pos()
            if againButton.collidepoint(mouse_pos):
                time.sleep(0.2)
                
                home_page=True
                play_vs_ai = False 
                game_over = False
                state = ttt.initial_state()



while True:

    screen.fill('black')
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if home_page:
        title = large_font.render("Ultimate TicTacToe", True, 'white')
        titleRect = title.get_rect()
        titleRect.center = (width/2, height/4)
        screen.blit(title, titleRect)

        playHumanButton = pygame.Rect(width/8, height*5/8, width/4, 50)
        playHuman = medium_font.render("Play vs Human", True, 'black')
        playHumanRect = playHuman.get_rect()
        playHumanRect.center = playHumanButton.center
        pygame.draw.rect(screen, 'white', playHumanButton)
        screen.blit(playHuman, playHumanRect)

        playAiButton = pygame.Rect(5*width/8, height*5/8, width/4, 50)
        playAi = medium_font.render("Play vs AI", True, 'black')
        playAiRect = playAi.get_rect()
        playAiRect.center = playAiButton.center
        pygame.draw.rect(screen, 'white', playAiButton)
        screen.blit(playAi, playAiRect)

        click, _, _ = pygame.mouse.get_pressed()
        
        if click:
            mouse_position = pygame.mouse.get_pos()

            if playHumanButton.collidepoint(mouse_position):
                time.sleep(0.5)
                play_vs_ai = False
                home_page = False
            
            elif playAiButton.collidepoint(mouse_position):
                time.sleep(0.5)
                play_vs_ai = True
                home_page = False

    # this will run when home_page = False, play_vs_ai = False
    # i.e. when we don't want to play against AI
    elif not play_vs_ai:

        display_board()

        click, _, _ = pygame.mouse.get_pressed()
         
        if click==1 and not game_over:
            mouse_position = pygame.mouse.get_pos()

            for R in range(3):
                for C in range(3):
                    for r in range(3):
                        for c in range(3):
                            if tiles[R][C][r][c].collidepoint(mouse_position) and ttt.legal_action(state, (R, C, r, c), True):
                                state = ttt.result(state, (R, C, r, c))
        
        


    # this runs when
    # 1) home_page = false
    # 2) play_vs_ai = True
    else:
        
        #runs when user hasn't select his role
        if user is None:
            title = large_font.render("Ultimate TicTacToe", True, 'white')
            titleRect = title.get_rect()
            titleRect.center = (width/2, height/4)
            screen.blit(title, titleRect)

            playXButton = pygame.Rect(width/8, height*5/8, width/4, 50)
            playX = medium_font.render("Play as X", True, 'black')
            playXRect = playX.get_rect()
            playXRect.center = playXButton.center
            pygame.draw.rect(screen, 'white', playXButton)
            screen.blit(playX, playXRect)
    
            playOButton = pygame.Rect(5*width/8, height*5/8, width/4, 50)
            playO = medium_font.render("Play as O", True, 'black')
            playORect = playO.get_rect()
            playORect.center = playOButton.center
            pygame.draw.rect(screen, 'white', playOButton)
            screen.blit(playO, playORect)

            click, _, _ = pygame.mouse.get_pressed()

            if click == 1:
                mouse_pos = pygame.mouse.get_pos()

                if playXButton.collidepoint(mouse_pos):
                    time.sleep(0.2)
                    user = ttt.X
                elif playOButton.collidepoint(mouse_pos):
                    time.sleep(0.2)
                    user = ttt.O
            
        # if user has selected their role, then play against AI
        else:

            display_board()
            pygame.display.flip()
            # player = ttt.player(state)

            if player==user and not game_over:

                click, _, _ = pygame.mouse.get_pressed()
         
                if click==1 and not game_over:
                    mouse_position = pygame.mouse.get_pos()

                    for R in range(3):
                        for C in range(3):
                            for r in range(3):
                                for c in range(3):
                                    if tiles[R][C][r][c].collidepoint(mouse_position) and ttt.legal_action(state, (R, C, r, c), True):
                                        state = ttt.result(state, (R, C, r, c))
            
            elif player!=user and not game_over:
                # time.sleep(1)
                ai_move = best_move(state, 5000)
                state = ttt.result(state, ai_move)

            





    pygame.display.flip()