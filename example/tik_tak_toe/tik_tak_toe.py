# Global variables for the Tik Tak Toe game
board = [[' ' for _ in range(3)] for _ in range(3)]  # 3x3 array of spaces (' ')
player = 'X'  # Current player initialized to 'X'
winner = ' '  # Indicates the game is ongoing

print("Tik Tak Toe game initialized.")  # Logging the initialization

def initialize_board():
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    print("Board initialized.")  # Logging board initialization

def display_board():
    print("\n")
    print(f' {board[0][0]} | {board[0][1]} | {board[0][2]} ')
    print("---+---+---")
    print(f' {board[1][0]} | {board[1][1]} | {board[1][2]} ')
    print("---+---+---")
    print(f' {board[2][0]} | {board[2][1]} | {board[2][2]} ')
    print("\n")
    print("Board displayed.")  # Logging board display

def check_winner():
    # Check rows and columns for a winner
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != ' ':
            print(f"Player {board[i][0]} wins by row.")  # Logging win by row
            return board[i][0]  # Winner in row
        if board[0][i] == board[1][i] == board[2][i] != ' ':
            print(f"Player {board[0][i]} wins by column.")  # Logging win by column
            return board[0][i]  # Winner in column
    
    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        print(f"Player {board[0][0]} wins by diagonal.")  # Logging win by diagonal
        return board[0][0]  # Winner in diagonal
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        print(f"Player {board[0][2]} wins by diagonal.")  # Logging win by diagonal
        return board[0][2]  # Winner in another diagonal
    
    # Check for any empty spaces, if found game is still ongoing
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                print("Game still ongoing.")  # Logging ongoing game
                return ' '  # Game still ongoing
    
    # If no winner and no empty spaces, it's a draw
    print("Game ended in a draw.")  # Logging draw
    return 'D'  # Draw

def play_game():
    global player, winner  # Access global variables
    initialize_board()  # Initialize the board
    display_board()  # Display the board
    
    while winner == ' ':  # Continue until game is over
        row = int(input(f"Player {player}, enter row (0, 1, 2): "))  # Get row input
        col = int(input(f"Player {player}, enter column (0, 1, 2): "))  # Get column input
        
        # Check if the chosen cell is empty
        if board[row][col] == ' ':
            board[row][col] = player  # Place player symbol in the cell
            display_board()  # Display the updated board
            winner = check_winner()  # Check if there is a winner
            player = 'O' if player == 'X' else 'X'  # Switch players
        else:
            print("Invalid move. Cell already taken. Try again.")  # Logging invalid move

    print(f"Game over. Winner: {winner}")  # Logging game over

# Start the game
play_game()