import chess
import chess.engine

difficulty_levels = {
    "easy": 2,
    "medium": 6,
    "hard": 12
}

engine = chess.engine.SimpleEngine.popen_uci("stockfish.exe")
engine.configure({"Skill Level": difficulty_levels[difficulty]})