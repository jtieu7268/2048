from board import Board
import pygame
from enum import Enum

# window related constants

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# header and score related constants
HEADER_WIDTH = SCREEN_WIDTH
HEADER_HEIGHT = SCREEN_HEIGHT / 8

# footer and key menu related constants
FOOTER_WIDTH = SCREEN_WIDTH
FOOTER_HEIGHT = SCREEN_HEIGHT / 8

# board related constants

BOARD_WIDTH = BOARD_HEIGHT = SCREEN_WIDTH
DIM = 4

LINE_THICKNESS = int(BOARD_WIDTH * 0.015)

TILE_WIDTH = (BOARD_WIDTH - LINE_THICKNESS * (DIM + 1)) // DIM
TILE_HEIGHT = (BOARD_HEIGHT - LINE_THICKNESS * (DIM + 1)) // DIM

VALUE_TO_COLOR = dict(zip([0] + [2**i for i in range(1,14)],
                        [(240,248,255),
                        (219,235,250),
                        (167,206,255),
                        (127,195,249),
                        (97,152,244),
                        (59,101,251),
                        (41,130,255),
                        (210,193,246),
                        (222,164,255),
                        (165,151,251),
                        (109,105,255),
                        (178,80,255)]))

# game related constants

class GameState(Enum):
    INTRO = -1
    PLAY = 0
    WIN = 1
    END = 2
    QUIT = 3
    RESTART = 4

GAME_KEY = {"W":"UP",
            "D":"RIGHT",
            "S":"DOWN",
            "A":"LEFT",
            "R":
            "RESTART",
            "Q":"QUIT"}
WIN_VAL_OPTIONS = ("2048", "1024", "512", "256", "128")

SCORE_BOX_WIDTH = (HEADER_WIDTH - 3 * LINE_THICKNESS) / 2
SCORE_BOX_HEIGHT = (HEADER_HEIGHT - LINE_THICKNESS)

# color constants

BACKGROUND_COLOR = (220,230,245) # line color
FONT_COLOR = (255,255,255)
FULL_SCREEN_COLOR = (240,248,255) # temporary empty square color

""" game states
- main: controls game state and pages, initiates pygame stuff
- intro: title page
- play: game loop
- win: player has won
- end: player has lost
- quit: player quits

intro: introduces game, gives option to select win val -> play
play: game loop, 
    needs score, high score,
    if player has won, give message with option to continue playing or quit -> win, 
    if game is over, take to end screen -> end
win: player has won, give message
    continue play -> play
    quit -> end
end: game was played and ended, give message
    if won, congratulations
    everyone gets high score and thanks for playing
    -> quit
quit: result from player quitting

board + play_2048 get gamestate enum?

"""

def game_intro(window):
    FONT_INTRO = pygame.font.SysFont("Arial", 60, bold=True)
    FONT_INTRO_SUB = pygame.font.SysFont("Arial", 30, bold=True)
    
    def draw_intro():
        window.fill(BACKGROUND_COLOR)
        welcome = FONT_INTRO.render("Welcome of 2048!", 1, FONT_COLOR)
        cont = FONT_INTRO_SUB.render("Press any key or click to continue", 1, FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 3 - (welcome.get_height() + cont.get_height()) / 2
        window.blits([(welcome, (SCREEN_WIDTH / 2 - welcome.get_width() / 2, start_text_height)),
                      (cont, (SCREEN_WIDTH / 2 - cont.get_width() / 2, SCREEN_HEIGHT / 2 - cont.get_height() / 2))])
        pygame.display.update()
    
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return GameState.PLAY
    
        draw_intro()

    return GameState.QUIT

def game_restart(window):

    FONT_RESTART = pygame.font.SysFont("Arial", 50, bold=True)

    def draw_restart(window):
        window.fill(BACKGROUND_COLOR)
        text = FONT_RESTART.render("What do you want the win value to be?", 1, FONT_COLOR)
        # TODO: buttons
        pygame.display.update()
    
    clock = pygame.tick(FPS)
    run = True
    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw_restart(window)

def game_loop(window, bd, high_score=0):
    
    FONT = pygame.font.SysFont("Arial", 50, bold=True)
    
    def draw_tiles(window, bd):
        def draw_tile(tile, r, c):
            x = (TILE_WIDTH + LINE_THICKNESS) * c + LINE_THICKNESS
            y = (TILE_HEIGHT + LINE_THICKNESS) * r + LINE_THICKNESS + HEADER_HEIGHT
            color = VALUE_TO_COLOR[tile]
            pygame.draw.rect(window, color, (x, y, TILE_WIDTH, TILE_HEIGHT), border_radius=TILE_WIDTH // 10)
            tile_text = str(tile) if tile else ""
            text = FONT.render(tile_text, 1, FONT_COLOR)
            window.blit(text,
                        (
                            x + TILE_WIDTH / 2 - text.get_width() / 2,
                            y + TILE_HEIGHT / 2 - text.get_height() / 2)
                        )

        for r, row in enumerate(bd.tiles):
            for c, tile in enumerate(row):
                draw_tile(tile, r, c)

    def draw_header(window, score, high_score):
        FONT_SCORE_HEADERS = pygame.font.SysFont('Arial', 30, bold=True)
        FONT_SCORES = pygame.font.SysFont('Arial', 28, bold=True)
        pygame.draw.rect(window, 
                         FULL_SCREEN_COLOR, 
                         (LINE_THICKNESS, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                         border_radius=int(SCORE_BOX_HEIGHT / 10)
                         )
        pygame.draw.rect(window, 
                         FULL_SCREEN_COLOR, 
                         (2 * LINE_THICKNESS + SCORE_BOX_WIDTH, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                         border_radius=int(SCORE_BOX_HEIGHT / 10)
                         )
        score_header = FONT_SCORE_HEADERS.render("SCORE", 1, BACKGROUND_COLOR)
        score_text = FONT_SCORES.render(str(score), 1, BACKGROUND_COLOR)
        high_score_header = FONT_SCORE_HEADERS.render("HIGH SCORE", 1, BACKGROUND_COLOR)
        high_score_text = FONT_SCORES.render(str(high_score), 1, BACKGROUND_COLOR)
        window.blits([(
            score_header, 
            (
                HEADER_WIDTH / 4 - score_header.get_width() / 2, 
                HEADER_HEIGHT / 4 - score_header.get_height() / 2
            )), (
            high_score_header,
            (
                HEADER_WIDTH - HEADER_WIDTH / 4 - high_score_header.get_width() / 2,
                HEADER_HEIGHT / 4 - high_score_header.get_height() / 2
            )), (
            score_text, 
            (
                HEADER_WIDTH / 4 - score_text.get_width() / 2,
                HEADER_HEIGHT - HEADER_HEIGHT / 4 - score_text.get_height() / 2
            )), (
            high_score_text, 
            (
                HEADER_WIDTH - HEADER_WIDTH / 4 - high_score_text.get_width() / 2,
                HEADER_HEIGHT - HEADER_HEIGHT / 4 - high_score_text.get_height() / 2
            ))
        ])

    def draw_footer(window):
        FONT_FOOTER = pygame.font.SysFont('Arial', 30, bold=True)
        pygame.draw.rect(window, 
                         FULL_SCREEN_COLOR, 
                         (LINE_THICKNESS, SCREEN_HEIGHT - FOOTER_HEIGHT, FOOTER_WIDTH - 2 * LINE_THICKNESS, FOOTER_HEIGHT - LINE_THICKNESS),
                         border_radius=int(FOOTER_HEIGHT / 10))
        instructions = FONT_FOOTER.render("Use arrow keys or WASD to slide tiles", 1, BACKGROUND_COLOR)
        options = FONT_FOOTER.render("R - RESTART    Q - QUIT", 1, BACKGROUND_COLOR)
        window.blits([(instructions, ((FOOTER_WIDTH - 2 * LINE_THICKNESS) / 2 - instructions.get_width() / 2, SCREEN_HEIGHT - 3 * FOOTER_HEIGHT / 4 - instructions.get_height() / 2)),
                     (options, ((FOOTER_WIDTH - 2 * LINE_THICKNESS) / 2 - options.get_width() / 2, SCREEN_HEIGHT - FOOTER_HEIGHT / 3 - options.get_height() / 2))])

    def draw(window, bd, score, high_score):
        window.fill(BACKGROUND_COLOR)
        draw_tiles(window, bd)
        draw_header(window, score, high_score)
        draw_footer(window)
        pygame.display.update()

    KEY_TO_MOVE = dict(zip([
                                pygame.K_UP, 
                                pygame.K_RIGHT, 
                                pygame.K_DOWN, 
                                pygame.K_LEFT] + [
                                pygame.K_w, 
                                pygame.K_d, 
                                pygame.K_s, 
                                pygame.K_a], 
                            [
                                "U", 
                                "R",
                                "D",
                                "L"
                            ] * 2))

    clock = pygame.time.Clock()
    run = True

    bd = Board(win_val=1024)
    score = 0

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_MOVE:
                    if bd.is_valid_move(KEY_TO_MOVE[event.key]):
                        score += bd.move(KEY_TO_MOVE[event.key])
                        bd.new_tile()
                        status = bd.is_end()
                        if score > high_score: high_score = score
                        if status == GameState.END.value:
                            return GameState(status), bd, high_score
                        if status == GameState.WIN.value:
                            draw(window, bd, score, high_score)
                            pygame.time.wait(1000)
                            return GameState.QUIT, bd, high_score
                if event.key == pygame.K_r:
                    return GameState.PLAY, bd, high_score
                if event.key == pygame.K_q:
                    return GameState.QUIT, bd, high_score
                            
        draw(window, bd, score, high_score)
    
    return GameState.QUIT, bd, high_score

def game_end(window, score):

    FONT_GAMEOVER = pygame.font.SysFont('Arial', 60, bold=True)
    FONT_MESSAGE = pygame.font.SysFont('Arial', 30, bold=True)

    def draw_end(window, score):
        window.fill(BACKGROUND_COLOR)
        gameover = FONT_GAMEOVER.render("GAME OVER", 1, FONT_COLOR)
        thanks = FONT_MESSAGE.render("Thanks for playing!", 1, FONT_COLOR)
        high_score = FONT_MESSAGE.render(f"High Score: {score}", 1, FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 2 - (thanks.get_height() + high_score.get_height()) / 2
        window.blits([
            (gameover, 
             (
                 SCREEN_WIDTH / 2 - gameover.get_width() / 2, 
                 SCREEN_HEIGHT / 4 - gameover.get_height() / 2
             )),
            (thanks, 
             (
                 SCREEN_WIDTH / 2 - thanks.get_width() / 2,
                 start_text_height
             ),),
            (high_score, 
             (
                 SCREEN_WIDTH / 2 - high_score.get_width() / 2,
                 start_text_height + thanks.get_height()
             ))])
        
        pygame.display.update()

    clock = pygame.time.Clock()
    run = True

    draw_end(window, score)

    while run:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return GameState.PLAY, score
                if event.key == pygame.K_q:
                    return GameState.QUIT, score
    
    return GameState.QUIT, score


def main():
    
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")

    game_state = GameState.INTRO
    high_score = 0
    bd = Board()

    while True:
        if game_state == GameState.INTRO:
            game_state = game_intro(window)
        if game_state == GameState.RESTART:
            game_state, bd = game_restart(window)
        if game_state == GameState.PLAY:
            game_state, bd, high_score = game_loop(window, bd, high_score)
        if game_state == GameState.QUIT:
            pygame.quit()
            return
        if game_state == GameState.END:
            game_state, high_score = game_end(window, high_score)


if __name__ ==  "__main__":
    main()