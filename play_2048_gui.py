from board import Board
import pygame
from enum import Enum

# window related constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
game_font = "Arial"

# header and score related constants
HEADER_WIDTH = SCREEN_WIDTH
HEADER_HEIGHT = SCREEN_HEIGHT // 8

# footer and key menu related constants
FOOTER_WIDTH = SCREEN_WIDTH
FOOTER_HEIGHT = SCREEN_HEIGHT // 8

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

GAME_KEY = {"W" : "UP",
            "D" : "RIGHT",
            "S" : "DOWN",
            "A" : "LEFT",
            "R" : "RESTART",
            "Q" : "QUIT"}
WIN_VAL_OPTIONS = ("2048", "1024", "512", "256", "128", "64", "32", "16")

SCORE_BOX_WIDTH = (HEADER_WIDTH - 3 * LINE_THICKNESS) // 2
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

# win state
# buttons for win state and lose state
# reset state
# enum - clean up in board and text version
# clean up text version
# consider efficient board
# ai

class StateManager:
    
    def __init__(self):
        self.change_state(IntroState())
        self.high_score = 0
        self.running = True

    def change_state(self, next_state):
        self.state = next_state
        self.state.manager = self

class State:

    def __init__(self):
        pass
    
    def handle_events(self):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError
    
    def render(self):
        raise NotImplementedError
    
class IntroState(State):

    def __init__(self):
        self.font = pygame.font.SysFont(game_font, 60, bold=True)
        self.font_sub = pygame.font.SysFont(game_font, 30, bold=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.change_state(ResetState()) # change to reset state once implemented

    def update(self):
        pass

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        welcome = self.font.render("Welcome of 2048!", 1, FONT_COLOR)
        cont = self.font_sub.render("Press any key or click to continue", 1, FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 3 - (welcome.get_height() + cont.get_height()) / 2
        window.blits([(welcome, (SCREEN_WIDTH / 2 - welcome.get_width() / 2, start_text_height)),
                      (cont, (SCREEN_WIDTH / 2 - cont.get_width() / 2, SCREEN_HEIGHT / 2 - cont.get_height() / 2))])
        pygame.display.update()

class ResetState(State):

    def __init__(self):
        self.font = pygame.font.SysFont(game_font, 30, bold=True)
        self.font_sub = pygame.font.SysFont(game_font, 40, bold=True)

    def handle_events(self, events):
        KEY_TO_WIN_VAL = dict(zip(
            (
                pygame.K_1, 
                pygame.K_2, 
                pygame.K_3, 
                pygame.K_4, 
                pygame.K_5, 
                pygame.K_6, 
                pygame.K_7, 
                pygame.K_8
            ), WIN_VAL_OPTIONS))
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_TO_WIN_VAL:
                    self.manager.change_state(BoardState(int(KEY_TO_WIN_VAL[event.key])))
    
    def update(self):
        pass

    def render(self, window):

        def draw_options():
            options = []
            for i, win_val in enumerate(WIN_VAL_OPTIONS):
                options.append(self.font_sub.render(f"({i+1}) {win_val}", 1, FONT_COLOR))
            OPTION_WIDTH = options[0].get_width() + LINE_THICKNESS
            OPTION_HEIGHT = options[0].get_height() + LINE_THICKNESS
            i = 0
            for c in [-1, 1]:
                x = SCREEN_WIDTH / 2 + c * SCREEN_WIDTH / 5 - OPTION_WIDTH / 2
                for r in range(4):
                    y = 2 * SCREEN_HEIGHT / 5 + r * (OPTION_HEIGHT + 2 * LINE_THICKNESS)
                    pygame.draw.rect(window, BACKGROUND_COLOR, (x, y, OPTION_WIDTH, OPTION_HEIGHT), border_radius=OPTION_HEIGHT // 10)
                    window.blit(options[i], 
                                (
                                    x + OPTION_WIDTH / 2 - options[0].get_width() / 2, 
                                    y + OPTION_HEIGHT / 2 - options[0].get_height() / 2
                                ))
                    i += 1
                    
        window.fill(FULL_SCREEN_COLOR)
        select_value = self.font.render("Enter a number to select a win value.", 1, FONT_COLOR)
        window.blit(select_value, (SCREEN_WIDTH / 2 - select_value.get_width() / 2, SCREEN_HEIGHT / 4 - select_value.get_height() / 2))
        draw_options()
        pygame.display.update()

class PlayState(State):

    def __init__(self):
        pass

    def handle_events(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def check_quit_reset(self, keydown):
        if keydown == pygame.K_r:
            self.manager.change_state(ResetState())
        if keydown == pygame.K_q:
            self.manager.change_state(EndState())

class BoardState(PlayState):

    def __init__(self, win_val=2048):
        self.font_tile = pygame.font.SysFont(game_font, 50, bold=True)
        self.font_score = pygame.font.SysFont(game_font, 28, bold=True)
        self.font = pygame.font.SysFont(game_font, 30, bold=True)

        self.score = 0
        self.bd = Board(win_val)
        self.won = False

    def handle_events(self, events):
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
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                super().check_quit_reset(event.key)
                if event.key in KEY_TO_MOVE:
                    if self.bd.is_valid_move(KEY_TO_MOVE[event.key]):
                        self.score += self.bd.move(KEY_TO_MOVE[event.key])
                        self.bd.new_tile()
                        status = self.bd.is_end(self.won)
                        if self.score > self.manager.high_score: self.manager.high_score = self.score
                        if status == GameState.END.value:
                            self.manager.change_state(LoseState(self))
                        if status == GameState.WIN.value:
                            self.won = True
                            self.manager.change_state(WinState(self))

    def update(self):
        pass
        
    def render(self, window):

        def draw_tiles():
            def draw_tile(tile, r, c):
                x = (TILE_WIDTH + LINE_THICKNESS) * c + LINE_THICKNESS
                y = (TILE_HEIGHT + LINE_THICKNESS) * r + LINE_THICKNESS + HEADER_HEIGHT
                color = VALUE_TO_COLOR[tile]
                pygame.draw.rect(window, color, (x, y, TILE_WIDTH, TILE_HEIGHT), border_radius=TILE_WIDTH // 10)
                tile_text = str(tile) if tile else ""
                text = self.font_tile.render(tile_text, 1, FONT_COLOR)
                window.blit(text,
                            (
                                x + TILE_WIDTH / 2 - text.get_width() / 2,
                                y + TILE_HEIGHT / 2 - text.get_height() / 2)
                            )
            for r, row in enumerate(self.bd.tiles):
                for c, tile in enumerate(row):
                    draw_tile(tile, r, c)

        def draw_header():
            pygame.draw.rect(window, 
                             FULL_SCREEN_COLOR, 
                             (LINE_THICKNESS, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                             border_radius=SCORE_BOX_HEIGHT // 10
                            )
            pygame.draw.rect(window, 
                             FULL_SCREEN_COLOR, 
                             (2 * LINE_THICKNESS + SCORE_BOX_WIDTH, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                             border_radius=SCORE_BOX_HEIGHT // 10
                            )
            score_header = self.font.render("SCORE", 1, BACKGROUND_COLOR)
            score_text = self.font_score.render(str(self.score), 1, BACKGROUND_COLOR)
            high_score_header = self.font.render("HIGH SCORE", 1, BACKGROUND_COLOR)
            high_score_text = self.font_score.render(str(self.manager.high_score), 1, BACKGROUND_COLOR)
            window.blits([
                (score_header, 
                 (
                     HEADER_WIDTH / 4 - score_header.get_width() / 2, 
                     HEADER_HEIGHT / 4 - score_header.get_height() / 2
                 )), 
                (high_score_header,
                 (
                     HEADER_WIDTH - HEADER_WIDTH / 4 - high_score_header.get_width() / 2, 
                     HEADER_HEIGHT / 4 - high_score_header.get_height() / 2
                 )), 
                (score_text, 
                 (
                     HEADER_WIDTH / 4 - score_text.get_width() / 2, 
                     HEADER_HEIGHT - HEADER_HEIGHT / 4 - score_text.get_height() / 2
                 )), 
                (high_score_text, 
                 (
                     HEADER_WIDTH - HEADER_WIDTH / 4 - high_score_text.get_width() / 2, 
                     HEADER_HEIGHT - HEADER_HEIGHT / 4 - high_score_text.get_height() / 2
                 ))])
        
        def draw_footer():
            pygame.draw.rect(window, 
                            FULL_SCREEN_COLOR, 
                            (LINE_THICKNESS, SCREEN_HEIGHT - FOOTER_HEIGHT, FOOTER_WIDTH - 2 * LINE_THICKNESS, FOOTER_HEIGHT - LINE_THICKNESS),
                            border_radius=FOOTER_HEIGHT // 10)
            instructions = self.font.render("Use arrow keys or WASD to slide tiles", 1, BACKGROUND_COLOR)
            options = self.font.render("R - RESTART    Q - QUIT", 1, BACKGROUND_COLOR)
            window.blits([
                (instructions, 
                 (
                     (FOOTER_WIDTH - 2 * LINE_THICKNESS) / 2 - instructions.get_width() / 2, 
                     SCREEN_HEIGHT - 3 * FOOTER_HEIGHT / 4 - instructions.get_height() / 2
                 )),
                (options, 
                 (
                     (FOOTER_WIDTH - 2 * LINE_THICKNESS) / 2 - options.get_width() / 2, 
                     SCREEN_HEIGHT - FOOTER_HEIGHT / 3 - options.get_height() / 2
                 ))])
        
        window.fill(BACKGROUND_COLOR)
        draw_tiles()
        draw_header()
        draw_footer()
        pygame.display.update()

class GameStatusState(PlayState):

    def __init__(self, game_state):
        self.font_title_message = pygame.font.SysFont(game_font, 55, bold=True)
        self.font = pygame.font.SysFont(game_font, 30, bold=True)

        self.game_state = game_state

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                super().check_quit_reset(event.key)
                if event.key == pygame.K_p:
                    self.manager.change_state(self.game_state)
                    return

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        score = self.font.render(f"Score: {self.game_state.score}", 1, FONT_COLOR)
        high_score = self.font.render(f"High Score: {self.manager.high_score}", 1, FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 2 - (score.get_height() + high_score.get_height()) / 2
        window.blits([
            (score, 
             (
                 SCREEN_WIDTH / 2 - score.get_width() / 2, 
                 start_text_height
             )), 
            (high_score, 
             (
                 SCREEN_WIDTH / 2 - high_score.get_width() / 2, 
                 start_text_height + score.get_height()
             )
            )])

class WinState(GameStatusState):

    def __init__(self, game_state):
        super().__init__(game_state)
        self.win_val = game_state.bd.WIN_VAL

    def render(self, window):
        super().render(window)
        congrats = self.font_title_message.render("CONGRATULATIONS!", 1, FONT_COLOR)
        win_message = self.font_title_message.render(f"YOU GOT {self.win_val}", 1, FONT_COLOR)
        choose = self.font.render("Select one of the following:", 1, FONT_COLOR)
        resume = self.font.render("(P) resume game", 1, FONT_COLOR)
        restart = self.font.render("(R) restart", 1, FONT_COLOR)
        quit = self.font.render("(Q) quit", 1, FONT_COLOR)
        start_text_height = 3 * SCREEN_HEIGHT / 4 - (choose.get_height() + resume.get_height() + restart.get_height()+ quit.get_height()) / 2
        window.blits([
            (congrats, 
             (
                 SCREEN_WIDTH / 2 - congrats.get_width() / 2, 
                 SCREEN_HEIGHT / 4 - (congrats.get_height() + win_message.get_height()) / 2
             )
            ), 
            (win_message,
             (
                 SCREEN_WIDTH / 2 - win_message.get_width() / 2,
                 SCREEN_HEIGHT / 4 - (congrats.get_height() + win_message.get_height()) / 2 + congrats.get_height()
             )
            ),
            (choose, 
             (
                 SCREEN_WIDTH / 2 - choose.get_width() / 2, 
                 start_text_height
             )
            ), 
            (resume,
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height()
             )
            ), 
            (restart,
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height() + resume.get_height()
             )
            ), 
            (quit, 
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height() + resume.get_height() + restart.get_height()
             )
            )])
        pygame.display.update()


class LoseState(GameStatusState):

    def __init__(self, game_state):
        super().__init__(game_state)

    def render(self, window):
        super().render(window)
        gameover = self.font_title_message.render("GAME OVER", 1, FONT_COLOR)
        choose = self.font.render("Select one of the following:", 1, FONT_COLOR)
        resume = self.font.render("(P) view board", 1, FONT_COLOR)
        restart = self.font.render("(R) restart", 1, FONT_COLOR)
        quit = self.font.render("(Q) quit", 1, FONT_COLOR)
        start_text_height = 3 * SCREEN_HEIGHT / 4 - (choose.get_height() + resume.get_height() + restart.get_height()+ quit.get_height()) / 2
        window.blits([
            (gameover, 
             (
                 SCREEN_WIDTH / 2 - gameover.get_width() / 2, 
                 SCREEN_HEIGHT / 4 - gameover.get_height() / 2
             )),
            (choose, 
             (
                 SCREEN_WIDTH / 2 - choose.get_width() / 2, 
                 start_text_height
             )
            ), 
            (resume,
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height()
             )
            ), 
            (restart,
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height() + resume.get_height()
             )
            ), 
            (quit, 
             (
                 SCREEN_WIDTH / 2 - resume.get_width() / 2, 
                 start_text_height + choose.get_height() + resume.get_height() + restart.get_height()
             )
            )])
        pygame.display.update()

class EndState(State):

    def __init__(self):
        self.font = pygame.font.SysFont(game_font, 55, bold=True)
        self.font_sub = pygame.font.SysFont(game_font, 35, bold=True)

    def handle_events(self, events):
        pass

    def update(self):
        self.manager.running = False

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        thanks = self.font.render("Thanks for playing!", 1, FONT_COLOR)
        high_score = self.font_sub.render(f"Your high score was {self.manager.high_score}", 1, FONT_COLOR)
        window.blits([
            (thanks, 
             (
                 SCREEN_WIDTH / 2 - thanks.get_width() / 2, 
                 SCREEN_HEIGHT / 2 - (thanks.get_height() + high_score.get_height()) / 2
             )), 
            (high_score, 
             (
                 SCREEN_WIDTH / 2 - high_score.get_width() / 2, 
                 SCREEN_HEIGHT / 2 - (thanks.get_height() + high_score.get_height()) / 2 + thanks.get_height()
             )
            )])
        pygame.display.update()
        pygame.time.wait(2000)

def main():
    
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")

    manager = StateManager()

    clock = pygame.time.Clock()
    # running = True

    while manager.running:

        clock.tick(FPS)
        
        if pygame.event.get(pygame.QUIT):
            manager.running = False
            return

        manager.state.handle_events(pygame.event.get())
        manager.state.update()
        manager.state.render(window)

        # if game_state == GameState.INTRO:
        #     high_score = 0
        #     bd = Board() # erase once restart is fixed
        #     game_state = game_intro(window)
        
        # if game_state == GameState.RESTART:
        #     game_state, bd = game_restart(window)
        
        # if game_state == GameState.PLAY:
        #     game_state, bd, high_score = game_loop(window, bd, high_score)
        
        # if game_state == GameState.QUIT:
        #     pygame.quit()
        #     return
        
        # if game_state == GameState.END:
        #     game_state, high_score = game_end(window, high_score)
    
    pygame.quit()

if __name__ ==  "__main__":
    main()


def game_intro(window):
    
    def draw_intro():
        FONT_INTRO = pygame.font.SysFont(game_font, 60, bold=True)
        FONT_INTRO_SUB = pygame.font.SysFont(game_font, 30, bold=True)
        window.fill(BACKGROUND_COLOR)
        welcome = FONT_INTRO.render("Welcome of 2048!", 1, FONT_COLOR)
        cont = FONT_INTRO_SUB.render("Press any key or click to continue", 1, FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 3 - (welcome.get_height() + cont.get_height()) / 2
        window.blits([(welcome, (SCREEN_WIDTH / 2 - welcome.get_width() / 2, start_text_height)),
                      (cont, (SCREEN_WIDTH / 2 - cont.get_width() / 2, SCREEN_HEIGHT / 2 - cont.get_height() / 2))])
        pygame.display.update()
    
    clock = pygame.time.Clock()
    intro = True

    while intro:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
                break

            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return GameState.PLAY
    
        draw_intro()

    return GameState.QUIT

def game_loop(window, bd, high_score=0):
    
    def draw_tiles(window, bd):
        
        FONT_TILE = pygame.font.SysFont(game_font, 50, bold=True)
        
        def draw_tile(tile, r, c):
            x = (TILE_WIDTH + LINE_THICKNESS) * c + LINE_THICKNESS
            y = (TILE_HEIGHT + LINE_THICKNESS) * r + LINE_THICKNESS + HEADER_HEIGHT
            color = VALUE_TO_COLOR[tile]
            pygame.draw.rect(window, color, (x, y, TILE_WIDTH, TILE_HEIGHT), border_radius=TILE_WIDTH // 10)
            tile_text = str(tile) if tile else ""
            text = FONT_TILE.render(tile_text, 1, FONT_COLOR)
            window.blit(text,
                        (
                            x + TILE_WIDTH / 2 - text.get_width() / 2,
                            y + TILE_HEIGHT / 2 - text.get_height() / 2)
                        )

        for r, row in enumerate(bd.tiles):
            for c, tile in enumerate(row):
                draw_tile(tile, r, c)

    def draw_header(window, score, high_score):
        FONT_SCORE_HEADERS = pygame.font.SysFont(game_font, 30, bold=True)
        FONT_SCORES = pygame.font.SysFont(game_font, 28, bold=True)
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
        FONT_FOOTER = pygame.font.SysFont(game_font, 30, bold=True)
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

    bd = Board(win_val=32)
    score = 0
    won = False

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
                        status = bd.is_end(won)
                        if score > high_score: high_score = score
                        if status == GameState.END.value:
                            return GameState(status), bd, high_score
                        if status == GameState.WIN.value:
                            won = True
                            draw(window, bd, score, high_score)
                            FONT_WIN = pygame.font.SysFont(game_font, 30, bold=True)
                            win_message = FONT_WIN.render("Congratulations, you won the game!", 1, FONT_COLOR)
                            pygame.draw.rect(window, BACKGROUND_COLOR, (SCREEN_WIDTH / 2 - win_message.get_width() / 2, SCREEN_HEIGHT / 2 - win_message.get_height() / 2, win_message.get_width(), win_message.get_height()))
                            window.blit(win_message, (SCREEN_WIDTH / 2 - win_message.get_width() / 2, SCREEN_HEIGHT / 2 - win_message.get_height() / 2))
                            pygame.display.update()
                            pygame.time.wait(2000)
                if event.key == pygame.K_r:
                    return GameState.PLAY, bd, high_score
                if event.key == pygame.K_q:
                    return GameState.QUIT, bd, high_score
                            
        draw(window, bd, score, high_score)
    
    return GameState.QUIT, bd, high_score

def game_end(window, score):

    FONT_GAMEOVER = pygame.font.SysFont(game_font, 60, bold=True)
    FONT_MESSAGE = pygame.font.SysFont(game_font, 30, bold=True)

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

def game_restart(window):

    def draw_restart(window):
        FONT_RESTART = pygame.font.SysFont(game_font, 50, bold=True)
        window.fill(BACKGROUND_COLOR)
        text = FONT_RESTART.render("What do you want the win value to be?", 1, FONT_COLOR)
        pygame.display.update()
    
    clock = pygame.time.Clock()
    restart = True

    win_val = 2048
    
    while restart:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT, None
            
            # change win_val based on button clicked

        draw_restart(window)
    
    return GameState.PLAY, Board(win_val)