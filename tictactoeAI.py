from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QGroupBox, QPushButton, QWidget, QVBoxLayout, QSizePolicy, QHBoxLayout
import sys
import random

class TicTacToe(QMainWindow):
    def __init__(self):
        super().__init__()
        self.states = {} #You can print states to see all possible winning/tie positions
        self.board = [" "] * 9
        self.character = "X" #Default character is X
        self.mode = "medium"
        self.createOutcomeMap(self.states)
        self.initUI()
    
    def initUI(self):
        self.setMinimumSize(600,800)
        
        #*Layout
        self.fields_groupbox = QGroupBox()
        self.fields_layout = QGridLayout()
        self.fields_groupbox.setLayout(self.fields_layout)
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.main_layout = QVBoxLayout()
        self.centralWidget.setLayout(self.main_layout)
        self.main_layout.addWidget(self.fields_groupbox)
        
        #*TicTacToe fields
        self.fields = []
        for i in range(9):
            field = QPushButton(" ")
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            field.setObjectName("field")
            field.clicked.connect(lambda checked, idx=i: self.field_Clicked(idx))
            self.fields.append(field)
            self.fields_layout.addWidget(field, i // 3, i % 3)
        self.fields_groupbox.setMaximumHeight(self.width())
        self.fields_groupbox.setGeometry(0,0,600,600)

        #*Difficulty button
        self.difficulty_buttons = QGroupBox()
        self.difficulty_layout = QHBoxLayout()
        self.difficulty_buttons.setLayout(self.difficulty_layout)
        self.easy_button = QPushButton("Easy mode")
        self.medium_button = QPushButton("Medium mode")
        self.hard_button = QPushButton("Impossible mode")
        self.easy_button.clicked.connect(lambda: self.set_mode("easy"))
        self.medium_button.clicked.connect(lambda: self.set_mode("medium"))
        self.hard_button.clicked.connect(lambda: self.set_mode("hard"))
        self.easy_button.setStyleSheet("background-color: #358554;")
        self.medium_button.setStyleSheet("background-color: #314385; border: 5px solid black;")
        self.hard_button.setStyleSheet("background-color: #672280;")
        self.easy_button.setMinimumSize(200,75)
        self.medium_button.setMinimumSize(200,75)
        self.hard_button.setMinimumSize(200,75)
        self.difficulty_layout.addWidget(self.easy_button)
        self.difficulty_layout.addWidget(self.medium_button)
        self.difficulty_layout.addWidget(self.hard_button)
        self.main_layout.addWidget(self.difficulty_buttons)

        #*Restart button
        self.restart_button = QPushButton("Restart")
        self.restart_button.setObjectName("restart")
        self.main_layout.addWidget(self.restart_button)
        self.restart_button.clicked.connect(self.resetBoard)
        self.restart_button.setMinimumSize(self.width(),75)
  
        #*Style sheets
        self.setStyleSheet("""
                
            #field{
                background-color: white;
                margin: 1px;
                border-radius: 5px;
                font-family: Times New Roman;
                font-weight: bold;
                font-size: 200px;
                border: 2px solid black;
                
            }               
            #restart{
                background-color: #ffacac;
                font-size: 50px;
                color: #ff5555;
            }
            QMainWindow{
                background-color: #9999ff;
            }
            QPushButton{
                font-size: 25px;
                font-family: Times New Roman;
            }
            
                           
                           """)
        
    def set_mode(self, mode):
        self.resetBoard()
        if mode == "easy":
            self.easy_button.setStyleSheet("background-color: #358554; border: 5px solid black;")
            self.medium_button.setStyleSheet("background-color: #314385;")
            self.hard_button.setStyleSheet("background-color: #672280;")
            self.mode = "easy"
            
        elif mode == "medium":
            self.mode = "medium"
            self.easy_button.setStyleSheet("background-color: #358554;")
            self.medium_button.setStyleSheet("background-color: #314385; border: 5px solid black;")
            self.hard_button.setStyleSheet("background-color: #672280;")
        else:
            self.mode = "hard"  
            self.easy_button.setStyleSheet("background-color: #358554;")
            self.medium_button.setStyleSheet("background-color: #314385;")
            self.hard_button.setStyleSheet("background-color: #672280; border: 5px solid black;")         
    
    def field_Clicked(self, buttonposition):
        if self.board[buttonposition] != " ":
            return
        
        winner = self.checkWinner( self.board, True)
        if " " in self.board and not winner:
            self.board[buttonposition] = self.character
            self.fields[buttonposition].setText(self.character) #mark the clicked field

            winner = self.checkWinner( self.board, True)
            
            if not winner:
                if self.character == "X" : #AI is the opposite
                    self.fields[buttonposition].setStyleSheet("color: #ff644d;") #red
                    if " " in self.board:
                        best_move = self.bestMove(self.board, "O") #calculate best move for ai
                        self.board[best_move] = "O" #apply ai's move
                        self.fields[best_move].setText("O")
                        self.fields[best_move].setStyleSheet("color: #1bcefe;") #blue
                    else:
                        for field in self.fields:
                            field.setStyleSheet("color: blue;")
                else:
                    self.fields[buttonposition].setStyleSheet("color: #1bcefe;") #blue
                    if " " in self.board:
                        best_move = self.bestMove(self.board, "X") #calculate best move for ai
                        self.board[best_move] = "X"
                        self.fields[best_move].setText("X")
                        self.fields[best_move].setStyleSheet("color: #ff644d;") #red
                    else:
                        for field in self.fields:
                            field.setStyleSheet("color: blue;")
            winner = self.checkWinner( self.board, True)
        elif " " not in self.board:
            for field in self.fields:
                field.setStyleSheet("color: blue;")
                    
    def resetBoard(self):
        for i in range(9):
            self.board[i] = " "
            self.fields[i].setText(" ")
            self.fields[i].setStyleSheet("")
             
    def createOutcomeMap(self, states, board=None, turn="X"): #!Function is not needed for main ai but just cool to see the outcome
        #*If theres no board, create one
        if board is None:
            board = [" "] * 9
            
             
        #*Look for winner    
        winner = self.checkWinner(board)
        if winner or " " not in board:
            state_key = "".join(board)
            states[state_key] = winner if winner else "Tie"
            return

        #*Go through all possible moves using recursion
        for i in range(9):
            if board[i] == " ":
                board[i] = turn #Set move
                self.createOutcomeMap(states, board, "O" if turn == "X" else "X") #Start recursion
                board[i] = " " #Reset board

    def checkWinner(self, board, haveToPaint=False):
        winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  #Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  #Columns
        [0, 4, 8], [2, 4, 6]              #Diagonals
        ]
        
        for combo in winning_combinations: #Look if any of the winning combinations is found
            if board[combo[0]] == board[combo[1]] == board[combo[2]] != " ":
                if haveToPaint: #If function is used from click function paint if someone won
                    self.fields[combo[0]].setStyleSheet(" color: purple;")
                    self.fields[combo[1]].setStyleSheet(" color: purple;")
                    self.fields[combo[2]].setStyleSheet(" color: purple;")
                return board[combo[0]]
        return None

    def minimax(self, board, is_maximizing, character, depth):
        winner = self.checkWinner(board)
        if character == "X": #In case AI is "X"
            if winner == character:
                return 100000 - depth
            elif winner == "O":
                return -1
            elif " " not in board:
                return 0
        else:               #In case AI is "O"
            if winner == character:
                return 100000 - depth
            elif winner == "X":
                return -1
            elif " " not in board:
                return 0
        
        if is_maximizing: #in case its ai's turn.. calculates the maximum
            best_score = -float("inf") #-inf so first found best score is always higher
            for i in range(9):
                if board[i] == " ":
                    board[i] = character
                    score = self.minimax(board, False, character, depth+1) #use recursion to find best score
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else: #in case its the enemy's turn.. calculates the lowest
            best_score = float("inf") #inf so first found best score is always lower
            for i in range(9):
                if board[i] == " ":
                    if character == "X":
                        board[i] = "O"
                    else:
                        board[i] = "X"
                    score = self.minimax(board, True, character, depth+1) #use recursion to find best score
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score
        
    def bestMove(self, board, character):
        best_score = -float("inf")
        move = -1
        for i in range(9):
            if board[i] == " ": 
                board[i] = character #Pretend move is set
                score = self.minimax(board, False, character, 0)
                board[i] = " " #Reset move
                if score > best_score: #If a better move is found set it to move
                    if self.mode == "easy": 
                        saveProbability = random.randint(1,3) #33% rarity to save best move on easy mode
                        if saveProbability == 1:  
                            best_score = score
                            if move == -1: #if no move was selected due to rarity, get first unused field
                                for j in range(9):
                                    if board[j] == " ":
                                        move = j           
                            else:
                                move = i
                    elif self.mode == "medium":
                        saveProbability = random.randint(1,4) #75% rarity to save best move on medium mode
                        if saveProbability < 3:  
                            best_score = score
                            move = i
                    else:
                        best_score = score #100% rarity to save best move on hard mode
                        move = i
                            
                    
        return move #Do the calculated best move
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TicTacToe()
    window.show()
    sys.exit(app.exec_())