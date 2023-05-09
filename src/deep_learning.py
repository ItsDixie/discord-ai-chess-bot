import chess
import chess.engine
import random
import json

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
    
    def train(self, num_games):

        try:
            self.insert_table()
            print('Table for train loaded')
        except Exception:
            pass

        board = chess.Board()
        print('---TRAINING...---')
        for i in range(num_games):
            while not board.is_game_over():
                try: 
                    next_state = self.get_board_state(board)
                    state = next_state
                    move = self.get_move(board)
                    board.push(move)
                    try:
                        score = self.engine.analyse(board, chess.engine.Limit(time=3.0))["score"].relative.score()
                    except Exception:
                        score = self.engine.analyse(board, chess.engine.Limit(time=10.0))["score"].relative.score()
                    reward = score / 100.0
                    action = list(board.move_stack)[-1].uci()
                    self.update_q_table(state, action, reward, next_state)
                    print(board)
                    print(f'score {reward} of this move')

                except Exception as e:
                    self.export_table()
                    print('---TRAINING FAIL RESTART---')
                    print(e)
                    self.train(num_games)
            print(f'Game over {board.result()}')
            board.reset()
        self.export_table()
        print('---TRAINING COMPLEATED---')
        self.close()

    
    def play_game(self):

        try:
            self.insert_table()
            print('Table loaded')
        except Exception:
            pass

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
        print("Game over!")
        self.export_table()
        self.close()
    
    def export_table(self):
        with open('table.json', 'w') as file:
            json.dump(self.q_table, file)

    def insert_table(self):
        with open('table.json', 'r') as file:
            self.q_table = json.load(file)

    def close(self):
        self.engine.quit()




bot = chessAI()
bot.train(10)

