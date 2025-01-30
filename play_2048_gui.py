from board import Board, BoardStatus, Move
import pygame
from enum import Enum

# window related constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60
GAME_FONT = "Arial"

# color constants
TILE_0002_COLOR = (190, 212, 233)
TILE_0004_COLOR = (103, 153, 203)
TILE_0008_COLOR = (153, 153, 204)
TILE_0016_COLOR = (103, 104, 171)
TILE_0032_COLOR = ( 88, 108, 156) 
TILE_0064_COLOR = (220, 181, 201)
TILE_0128_COLOR = (195, 131, 152)
TILE_0256_COLOR = (206, 128, 167)
TILE_0512_COLOR = ( 82, 125, 115)
TILE_1024_COLOR = ( 94, 141, 131)
TILE_2048_COLOR = ( 95, 119, 141)
TILE_4096_COLOR = (136, 136, 183)
TILE_8192_COLOR = (213, 188, 213)

TILE_FONT_COLOR = (255,255,255)
EMPTY_TILE_COLOR = BACKGROUND_COLOR = (231, 241, 251)
TEXT_FONT_COLOR = GRID_LINE_COLOR = (81, 102, 121)
BUTTON_TEXT_COLOR = TILE_FONT_COLOR
BUTTON_COLOR = TILE_0002_COLOR
BUTTON_HOVER_COLOR = GRID_LINE_COLOR

# header and score related constants
HEADER_WIDTH = SCREEN_WIDTH
HEADER_HEIGHT = SCREEN_HEIGHT // 8

# footer and key menu related constants
FOOTER_WIDTH = SCREEN_WIDTH
FOOTER_HEIGHT = SCREEN_HEIGHT // 8

# board related constants
BOARD_WIDTH = BOARD_HEIGHT = SCREEN_WIDTH
DIM = 4 # number of rows/columns

LINE_THICKNESS = int(BOARD_WIDTH * 0.015)

TILE_WIDTH = (BOARD_WIDTH - LINE_THICKNESS * (DIM + 1)) // DIM
TILE_HEIGHT = (BOARD_HEIGHT - LINE_THICKNESS * (DIM + 1)) // DIM

VALUE_TO_COLOR = dict(zip([0] + [2**i for i in range(1,14)],
                        [EMPTY_TILE_COLOR,
                        TILE_0002_COLOR,
                        TILE_0004_COLOR,
                        TILE_0008_COLOR,
                        TILE_0016_COLOR,
                        TILE_0032_COLOR,
                        TILE_0064_COLOR,
                        TILE_0128_COLOR,
                        TILE_0256_COLOR,
                        TILE_0512_COLOR,
                        TILE_1024_COLOR,
                        TILE_2048_COLOR, 
                        TILE_4096_COLOR, 
                        TILE_8192_COLOR]))

# game related constants
class GameStatus(Enum):
    PLAY = 0
    QUIT = 1
    RESTART = 2

WIN_VAL_OPTIONS = (2048, 1024, 512, 256, 128, 64, 32, 16)

SCORE_BOX_WIDTH = (HEADER_WIDTH - 3 * LINE_THICKNESS) // 2
SCORE_BOX_HEIGHT = (HEADER_HEIGHT - LINE_THICKNESS)

# consider animations
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

    def get_high_score(self):
        return self.high_score

    def set_high_score(self, high_score):
        self.high_score = high_score

    def end_game(self):
        self.running = False

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
        self.font = pygame.font.SysFont(GAME_FONT, 60, bold=True)
        self.font_sub = pygame.font.SysFont(GAME_FONT, 30, bold=True)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.change_state(ResetState())

    def update(self):
        pass

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        welcome = self.font.render("Welcome of 2048!", 1, TEXT_FONT_COLOR)
        cont = self.font_sub.render("Press any key or click to continue", 1, TEXT_FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 3 - (welcome.get_height() + cont.get_height()) / 2
        window.blits([(welcome, (SCREEN_WIDTH / 2 - welcome.get_width() / 2, start_text_height)),
                      (cont, (SCREEN_WIDTH / 2 - cont.get_width() / 2, SCREEN_HEIGHT / 2 - cont.get_height() / 2))])
        pygame.display.update()

class ResetState(State):

    OPTION_WIDTH = SCREEN_WIDTH // 3
    OPTION_HEIGHT = OPTION_WIDTH // 4

    def __init__(self):
        self.font = pygame.font.SysFont(GAME_FONT, 30, bold=True)
        self.font_sub = pygame.font.SysFont(GAME_FONT, 40, bold=True)
        self.make_buttons()

    def make_buttons(self):
        self.buttons = []

        for i, win_val in enumerate(WIN_VAL_OPTIONS):
            r = i % DIM
            c = -1 if i // DIM == 0 else 1
            x = SCREEN_WIDTH / 2 + c * SCREEN_WIDTH / 5 - self.OPTION_WIDTH / 2
            y = 2 * SCREEN_HEIGHT / 5 + r * (self.OPTION_HEIGHT + 2 * LINE_THICKNESS)
            left = self.buttons[(i // DIM) * DIM].get_text_left() if r else None
            self.buttons.append(
                Button(
                        rect = (x, y, self.OPTION_WIDTH, self.OPTION_HEIGHT), 
                        text = f"({i+1}) {win_val}", 
                        font = self.font_sub, 
                        font_color = BUTTON_TEXT_COLOR, 
                        button_color = BUTTON_COLOR, 
                        button_hover_color = BUTTON_HOVER_COLOR, 
                        click_action = win_val, 
                        subsequent_button = left
                    ))

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
                    self.manager.change_state(BoardState(KEY_TO_WIN_VAL[event.key]))
            for button in self.buttons:
                win_val = button.check_event(event)
                if win_val:
                    self.manager.change_state(BoardState(win_val))
    
    def update(self):
        for button in self.buttons:
            button.update()

    def render(self, window):                    
        window.fill(BACKGROUND_COLOR)
        select_value = self.font.render("Enter a number to select a win value.", 1, TEXT_FONT_COLOR)
        window.blit(select_value, (SCREEN_WIDTH / 2 - select_value.get_width() / 2, SCREEN_HEIGHT / 4 - select_value.get_height() / 2))
        for button in self.buttons:
            button.render(window)
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
        self.font_tile = pygame.font.SysFont(GAME_FONT, 50, bold=True)
        self.font_score = pygame.font.SysFont(GAME_FONT, 28, bold=True)
        self.font = pygame.font.SysFont(GAME_FONT, 30, bold=True)

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
                                Move.UP, 
                                Move.RIGHT,
                                Move.DOWN,
                                Move.LEFT
                            ] * 2))
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                super().check_quit_reset(event.key)
                if event.key in KEY_TO_MOVE:
                    if self.bd.is_valid_move(KEY_TO_MOVE[event.key]):
                        self.score += self.bd.move(KEY_TO_MOVE[event.key])
                        self.bd.new_tile()
                        status = self.bd.is_end(self.won)
                        if self.score > self.manager.get_high_score(): self.manager.set_high_score(self.score)
                        if status == BoardStatus.GAMEOVER:
                            self.manager.change_state(LoseState(self))
                        if status == BoardStatus.WIN:
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
                text = self.font_tile.render(tile_text, 1, TILE_FONT_COLOR)
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
                             EMPTY_TILE_COLOR, 
                             (LINE_THICKNESS, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                             border_radius=SCORE_BOX_HEIGHT // 10
                            )
            pygame.draw.rect(window, 
                             EMPTY_TILE_COLOR, 
                             (2 * LINE_THICKNESS + SCORE_BOX_WIDTH, LINE_THICKNESS, SCORE_BOX_WIDTH, SCORE_BOX_HEIGHT), 
                             border_radius=SCORE_BOX_HEIGHT // 10
                            )
            score_header = self.font.render("SCORE", 1, TEXT_FONT_COLOR)
            score_text = self.font_score.render(str(self.score), 1, TEXT_FONT_COLOR)
            high_score_header = self.font.render("HIGH SCORE", 1, TEXT_FONT_COLOR)
            high_score_text = self.font_score.render(str(self.manager.get_high_score()), 1, TEXT_FONT_COLOR)
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
                            EMPTY_TILE_COLOR, 
                            (LINE_THICKNESS, SCREEN_HEIGHT - FOOTER_HEIGHT, FOOTER_WIDTH - 2 * LINE_THICKNESS, FOOTER_HEIGHT - LINE_THICKNESS),
                            border_radius=FOOTER_HEIGHT // 10)
            instructions = self.font.render("Use arrow keys or WASD to slide tiles", 1, TEXT_FONT_COLOR)
            options = self.font.render("R - RESTART    Q - QUIT", 1, TEXT_FONT_COLOR)
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
        
        window.fill(GRID_LINE_COLOR)
        draw_tiles()
        draw_header()
        draw_footer()
        pygame.display.update()

class GameStatusState(PlayState):

    OPTION_WIDTH = SCREEN_WIDTH // 2
    OPTION_HEIGHT = OPTION_WIDTH // 6

    def __init__(self, game_state):
        self.font_title_message = pygame.font.SysFont(GAME_FONT, 55, bold=True)
        self.font = pygame.font.SysFont(GAME_FONT, 30, bold=True)

        self.game_state = game_state
        self.options = ["(P) ", "(R) RESTART", "(Q) QUIT"]
        self.states = [GameStatus.PLAY, GameStatus.RESTART, GameStatus.QUIT]
        self.buttons = []
        self.start_text_height = 3 * SCREEN_HEIGHT / 4 - (len(self.options) * (self.OPTION_HEIGHT + LINE_THICKNESS) + self.OPTION_HEIGHT) / 2

    def make_buttons(self):
        for i, option in enumerate(self.options):
            self.buttons.append(
                Button(
                        rect = (SCREEN_WIDTH / 2 - self.OPTION_WIDTH / 2, self.start_text_height + i * (self.OPTION_HEIGHT + LINE_THICKNESS) + self.OPTION_HEIGHT, self.OPTION_WIDTH, self.OPTION_HEIGHT), 
                        text = option, 
                        font = self.font, 
                        font_color = BUTTON_TEXT_COLOR, 
                        button_color = BUTTON_COLOR, 
                        button_hover_color = BUTTON_HOVER_COLOR, 
                        click_action = self.states[i]
                        ))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                super().check_quit_reset(event.key)
                if event.key == pygame.K_p:
                    self.manager.change_state(self.game_state)
                    return
            for button in self.buttons:
                next_state = button.check_event(event)
                if next_state == GameStatus.PLAY:
                    self.manager.change_state(self.game_state)
                elif next_state == GameStatus.RESTART:
                    self.manager.change_state(ResetState())
                elif next_state == GameStatus.QUIT:
                    self.manager.change_state(EndState())

    def update(self):
        for button in self.buttons:
            button.update()

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        score = self.font.render(f"Score: {self.game_state.score}", 1, TEXT_FONT_COLOR)
        high_score = self.font.render(f"High Score: {self.manager.get_high_score()}", 1, TEXT_FONT_COLOR)
        start_text_height = SCREEN_HEIGHT / 2 - (score.get_height() + high_score.get_height()) / 2
        choose = self.font.render("Select one of the following:", 1, TEXT_FONT_COLOR)
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
            ),
            (choose, 
             (
                 SCREEN_WIDTH / 2 - choose.get_width() / 2, 
                 self.start_text_height
             )
            )])
        for button in self.buttons:
            button.render(window)

class WinState(GameStatusState):

    def __init__(self, game_state):
        super().__init__(game_state)
        self.win_val = game_state.bd.WIN_VAL
        self.options[0] += "RESUME GAME"
        self.make_buttons()

    def render(self, window):
        super().render(window)
        congrats = self.font_title_message.render("CONGRATULATIONS!", 1, TEXT_FONT_COLOR)
        win_message = self.font_title_message.render(f"YOU GOT {self.win_val}", 1, TEXT_FONT_COLOR)
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
            )])
        pygame.display.update()

class LoseState(GameStatusState):

    def __init__(self, game_state):
        super().__init__(game_state)
        self.options[0] += "VIEW BOARD"
        self.make_buttons()

    def render(self, window):
        super().render(window)
        gameover = self.font_title_message.render("GAME OVER", 1, TEXT_FONT_COLOR)
        window.blits([
            (gameover, 
             (
                 SCREEN_WIDTH / 2 - gameover.get_width() / 2, 
                 SCREEN_HEIGHT / 4 - gameover.get_height() / 2
             )
            )])
        pygame.display.update()

class EndState(State):

    def __init__(self):
        self.font = pygame.font.SysFont(GAME_FONT, 55, bold=True)
        self.font_sub = pygame.font.SysFont(GAME_FONT, 35, bold=True)

    def handle_events(self, events):
        pass

    def update(self):
        self.manager.end_game()

    def render(self, window):
        window.fill(BACKGROUND_COLOR)
        thanks = self.font.render("Thanks for playing!", 1, TEXT_FONT_COLOR)
        high_score = self.font_sub.render(f"Your high score was {self.manager.get_high_score()}", 1, TEXT_FONT_COLOR)
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

class Button:

    def __init__(self, rect: tuple[int,int,int,int], text: str, font: pygame.font.Font, font_color: tuple[int,int,int], button_color: tuple[int,int,int], button_hover_color: tuple[int,int,int], click_action: int, subsequent_button: int=0):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.font_color = font_color
        self.text = self.font.render(text, 1, self.font_color)
        self.curr_color = self.button_color = button_color
        self.button_hover_color = button_hover_color
        self.click_action = click_action
        self.clicked = False
        self.hovered = False
        self.subsequent_button = subsequent_button

    def check_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos):
            self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.clicked:
            self.clicked = False
            return self.click_action
        return 0

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()) and not self.hovered:
            self.hovered = True
        elif not self.rect.collidepoint(pygame.mouse.get_pos()) and self.hovered:
            self.hovered = False

    def update(self):
        self.curr_color = self.button_color
        self.check_hover()
        if self.hovered:
            self.curr_color = self.button_hover_color
        

    def render(self, window):
        pygame.draw.rect(window, self.curr_color, self.rect, border_radius=self.rect.height // 5)
        if not self.subsequent_button:
            text_rect = self.text.get_rect(center=self.rect.center)
        else:
            text_rect = self.text.get_rect(left=self.subsequent_button, centery=self.rect.centery)
        window.blit(self.text, text_rect)

    def get_text_left(self):
        return self.text.get_rect(center=self.rect.center).left

def main():
    
    pygame.init()

    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")

    manager = StateManager()

    clock = pygame.time.Clock()

    while manager.running:

        clock.tick(FPS)
        
        if pygame.event.get(pygame.QUIT):
            manager.end_game()
            return

        manager.state.handle_events(pygame.event.get())
        manager.state.update()
        manager.state.render(window)
    
    pygame.quit()

if __name__ ==  "__main__":
    main()
