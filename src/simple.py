import chess.engine
import random
import chess.svg

class ChessBot:
    def __init__(self):
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci("Rybka.exe")
            self.board = chess.Board()
        except Exception:
            pass
        
    def play(self):
        while not self.board.is_game_over():
            if self.board.turn == chess.BLACK:
                move = self.get_best_move()
                self.board.push(move)
            else:
                try:
                    move = input("Enter your move: ")
                    self.board.push_san(move)
                except Exception:
                    print("Wrong input (use coordinate table)")

            self.display(move)
            
        print("Game over")
        
    def get_best_move(self):
        result = self.engine.play(self.board, chess.engine.Limit(time=2.0))
        return result.move
    
    def train(self, num_games):
        for i in range(num_games):
            while not self.board.is_game_over():
                move = self.get_random_move()
                self.board.push(move)
                
                self.board.push(self.get_best_move())
                print("--------------")
                print(self.board)
                print("--------------")
            print(f'Game over {self.board.result()}')
            self.board.reset()
            
    def get_random_move(self):
        legal_moves = list(self.board.legal_moves)
        return random.choice(legal_moves)
    
    def close(self):
        self.engine.quit()

    def display(self, move=None):
        self.boardsvg = chess.svg.board(board=self.board, size=350)
        with open('output.svg', 'w') as file:
            file.write(self.boardsvg)
            


bot = ChessBot()
bot.play()
bot.close()
