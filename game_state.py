import pygame
import chess
import chess.engine
from game_state_base import GameState
from match_reorder_JSON import MatchRecorder
import os

title_size = 80

def compute_board_offset(screen_width, screen_height):
    board_width = 8 * title_size
    board_height = 8 * title_size

    x = (screen_width - board_width) // 2
    y = (screen_height - board_height) // 2

    return x, y

light = (240, 217, 181)
dark = (181, 136, 99)

class Game(GameState):
    def __init__(self, manager):
        self.board_offset = (0, 0)
        self.manager = manager
        self.font = pygame.font.SysFont("Arial", 20)
        self.recorder = MatchRecorder()

    def enter(self, params=None):
        if params is None:
            self.player_color = "white"
            self.difficulty = 2
        else:
            self.player_color = params.get("color", "white")
            self.difficulty = params.get("difficulty", 2)

        self.board = chess.Board()

        self.engine = chess.engine.SimpleEngine.popen_uci(
            r"C:\stockfish-windows-x86-64-avx2.exe"
        )
        self.engine.configure({"Skill Level": self.difficulty})

        self.selected_square = None
        self.legal_moves = []

        self.load_piece_images()

        if self.player_color == "black":
            self.make_ai_move()

    def load_piece_images(self):
        self.piece_images = {}
        pieces = ["p", "r", "n", "b", "q", "k"]

        for piece in pieces:
            white = pygame.image.load(os.path.join(f"assets/images/{piece}_white.png"))
            black = pygame.image.load(os.path.join(f"assets/images/{piece}_black.png"))

            self.piece_images[piece.upper()] = pygame.transform.scale(white, (title_size, title_size))
            self.piece_images[piece.lower()] = pygame.transform.scale(black, (title_size, title_size))

    def draw_board(self, screen):
        for rank in range(8):
            for file in range(8):
                color = light if (rank + file) % 2 == 0 else dark
                bx, by = self.board_offset
                rect = pygame.Rect(bx + file * title_size,
                                   by + rank * title_size,
                                   title_size, title_size)
                pygame.draw.rect(screen, color, rect)

    def draw_pieces(self, screen):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                img = self.piece_images[piece.symbol()]
                file = chess.square_file(square)
                rank = 7 - chess.square_rank(square)

                bx, by = self.board_offset
                screen.blit(
                    img,
                    (bx + file * title_size,
                     by + rank * title_size)
                )

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)

    def render(self, screen):
        screen.fill((0, 0, 0))

        w, h = screen.get_size()
        self.board_offset = compute_board_offset(w, h)

        self.draw_board(screen)
        self.draw_pieces(screen)
        self.draw_selected_square(screen)
        self.draw_legal_moves(screen)
        self.draw_hover(screen)
    def handle_click(self, pos):
        x, y = pos
        bx, by = self.board_offset

        if not (bx <= x < bx + 8 * title_size and by <= y < by + 8 * title_size):
            return

        file = (x - bx) // title_size
        rank = 7 - (y - by) // title_size
        square = chess.square(file, rank)

        piece = self.board.piece_at(square)

        # first click: select desired piece
        if self.selected_square is None:
            is_white = self.player_color == "white"
            if piece and piece.color == is_white:
                self.selected_square = square
                self.legal_moves = [
                    move for move in self.board.legal_moves
                    if move.from_square == square
                ]
            return

        # second click: attempt move
        move = chess.Move(self.selected_square, square)
        if move in self.legal_moves:
            self.board.push(move)
            self.selected_square = None
            self.legal_moves = []

            if self.board.is_game_over():
                self.finish_game()
            else:
                self.make_ai_move()
        else:
            self.selected_square = None
            self.legal_moves = []

    def make_ai_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
        self.board.push(result.move)

        if self.board.is_game_over():
            self.finish_game()

    def draw_selected_square(self, screen):
        if self.selected_square is None:
            return

        file = chess.square_file(self.selected_square)
        rank = 7 - chess.square_rank(self.selected_square)

        bx, by = self.board_offset
        rect = pygame.Rect(bx + file * title_size,
                           by + rank * title_size,
                           title_size, title_size)

        pygame.draw.rect(screen, (255, 255, 0, 80), rect, 4)

    def draw_legal_moves(self, screen):
        for move in self.legal_moves:
            file = chess.square_file(move.to_square)
            rank = 7 - chess.square_rank(move.to_square)

            bx, by = self.board_offset
            center_x = bx + file * title_size + title_size // 2
            center_y = by + rank * title_size + title_size // 2

            pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), 10)

    def draw_hover(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        bx, by = self.board_offset

        if not (bx <= mouse_x < bx + 8 * title_size and by <= mouse_y < by + 8 * title_size):
            return

        file = (mouse_x - bx) // title_size
        rank = 7 - (mouse_y - by) // title_size

        #bx, by = self.board_offset
        rect = pygame.Rect(bx + file * title_size,
                           by + rank * title_size,
                           title_size, title_size)

        pygame.draw.rect(screen, (0, 0, 255), rect, 2)

    def finish_game(self):
        result = self.board.result()

        if result == "1-0":
            outcome = "win" if self.player_color == "white" else "loss"
        elif result == "0-1":
            outcome = "win" if self.player_color == "black" else "loss"
        else:
            outcome = "draw"

        self.recorder.record(
            color=self.player_color,
            difficulty=self.difficulty,
            result=outcome,
            moves=len(self.board.move_stack)
        )

        self.engine.quit()

        self.manager.set_state("result_screen", {
            "result": outcome,
            "moves": len(self.board.move_stack)
        })

class ResultScreen(GameState):
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.Font(None, 60)

        # Button rectangle (x, y, width, height)
        self.button_rect = pygame.Rect(200, 300, 250, 60)

    def enter(self, params=None):
        if params is None:
            self.result = "unknown"
            self.moves = 0
        else:
            self.result = params["result"]
            self.moves = params["moves"]

    def update(self, events):
        for event in events:

            # Handle mouse click on button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.manager.set_state("main_menu")

            # Allow keyboard shortcut too
            if event.type == pygame.KEYDOWN:
                self.manager.set_state("main_menu")

    def render(self, screen):
        screen.fill((20, 20, 20))

        # Draw result text
        text = self.font.render(f"Results: {self.result}", True, (255, 255, 255))
        screen.blit(text, (200, 200))

        # Draw button
        pygame.draw.rect(screen, (70, 70, 200), self.button_rect)
        label = self.font.render("Main Menu", True, (255, 255, 255))
        screen.blit(label, (self.button_rect.x + 10, self.button_rect.y + 10))