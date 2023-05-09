import chess
import chess.engine
import random

class chessAI:

    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("Rybka.exe")
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.6
        self.epsilon = 0.1

    def get_move(self, board):
    
        state = self.get_board_state(board)
        
        legal_moves = list(board.legal_moves)
        
        if (state not in self.q_table):
            self.q_table[state] = [0] * len(legal_moves)
        
        if (random.random() < self.epsilon):
        
            return random.choice(legal_moves)
        
        else:
            best_move_index = self.q_table[state].index(max(self.q_table[state]))
            return legal_moves[best_move_index]
        
    def update_q_table(self, state, action, reward, next_state):
        legal_moves = list(chess.Board(next_state).legal_moves)
        
        if (next_state not in self.q_table):
        
            self.q_table[next_state] = [0] * len(legal_moves)
            
        max_q = max(self.q_table[next_state])
        action = legal_moves.index(chess.Move.from_uci(action))
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_q - self.q_table[state][action])

    def get_board_state(self, board):
        return board.fen()
    
    def play_game(self):
        board = chess.Board()

        while not board.is_game_over():
            next_state = self.get_board_state(board)
            state = next_state
            if(board.turn == chess.BLACK):
                move = self.get_move(board)
                board.push(move)
                score = self.engine.analyse(board, chess.engine.Limit(time=1.0))["score"].relative.score()
                reward = score / 100.0
                action = list(board.move_stack)[-1].uci()
                self.update_q_table(state, action, reward, next_state)
            else:
                try:
                    move = input("Enter your move: ")
                    board.push_san(move)
                except Exception:
                    print("Wrong input (use coordinate table)")
            print(board)




bot = chessAI()
bot.play_game()
