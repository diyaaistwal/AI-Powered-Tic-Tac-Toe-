import tkinter as tk
import random

# Create the main application window
root = tk.Tk()
root.title("Tic Tac Toe with AI Learning")
root.geometry("600x600")
root.configure(bg="#87CEFA")  # Light blue background

# Variables for the game
player_symbol = "X"
ai_symbol = "O"
board = [""] * 9
current_turn = "Player"
rounds_played = 0
max_rounds = 3
player_score = 0
ai_score = 0

# Memory for AI learning: Tracks move outcomes
ai_memory = {i: {"win": 0, "loss": 0, "tie": 0} for i in range(9)}

# Function to check for a win
def check_winner(symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for condition in win_conditions:
        if all(board[i] == symbol for i in condition):
            return True
    return False

# Function to handle button click
def button_click(index):
    global current_turn, rounds_played, player_score, ai_score

    if board[index] == "" and current_turn == "Player":
        board[index] = player_symbol
        update_button(index, player_symbol)

        if check_winner(player_symbol):
            result_label.config(text="Player Wins!")
            player_score += 1
            update_ai_memory("loss")  # Player win means AI loss
            end_round()
        elif "" not in board:
            result_label.config(text="It's a Tie!")
            update_ai_memory("tie")  # Tie result
            end_round()
        else:
            current_turn = "AI"
            ai_turn()

# Function for AI's turn
def ai_turn():
    global current_turn, rounds_played, player_score, ai_score

    empty_indices = [i for i in range(len(board)) if board[i] == ""]
    if empty_indices:
        # AI makes a move based on learning
        ai_choice = ai_decision(empty_indices)
        board[ai_choice] = ai_symbol
        update_button(ai_choice, ai_symbol)

        if check_winner(ai_symbol):
            result_label.config(text="AI Wins!")
            ai_score += 1
            update_ai_memory("win")  # AI win
            end_round()
        elif "" not in board:
            result_label.config(text="It's a Tie!")
            update_ai_memory("tie")  # Tie result
            end_round()
        else:
            current_turn = "Player"

# Function for AI decision-making
# Function for AI decision-making
def ai_decision(empty_indices):
    # 1. Check if AI can win
    for move in empty_indices:
        board[move] = ai_symbol
        if check_winner(ai_symbol):
            board[move] = ""  # Reset for testing
            return move
        board[move] = ""

    # 2. Check if the player can win and block them
    for move in empty_indices:
        board[move] = player_symbol
        if check_winner(player_symbol):
            board[move] = ""  # Reset for testing
            return move
        board[move] = ""

    # 3. Prioritize center, then corners
    if 4 in empty_indices:  # Center
        return 4
    for move in [0, 2, 6, 8]:  # Corners
        if move in empty_indices:
            return move

    # 4. Use learning-based decision as a fallback
    best_score = -float("inf")
    best_move = random.choice(empty_indices)  # Default to random choice
    for move in empty_indices:
        score = ai_memory[move]["win"] - ai_memory[move]["loss"]
        if score > best_score:
            best_score = score
            best_move = move
    return best_move


# Function to update AI memory based on game outcome
def update_ai_memory(outcome):
    for i, move in enumerate(board):
        if move == ai_symbol:
            if outcome == "win":
                ai_memory[i]["win"] += 1
            elif outcome == "loss":
                ai_memory[i]["loss"] += 1
            elif outcome == "tie":
                ai_memory[i]["tie"] += 1

# Function to update button with glowing effect
def update_button(index, symbol):
    if symbol == "X":
        buttons[index].config(
            text=symbol, fg="#FF5733", font=("Helvetica", 32, "bold"),
            bg="#FFCCCC", activebackground="#FF9999"
        )
    else:
        buttons[index].config(
            text=symbol, fg="#33FF57", font=("Helvetica", 32, "bold"),
            bg="#CCFFCC", activebackground="#99FF99"
        )

# Function to end the current round
def end_round():
    global rounds_played, board, current_turn

    rounds_played += 1
    if rounds_played >= max_rounds:
        display_final_result()
    else:
        reset_board()

# Function to reset the game board
def reset_board():
    global board, current_turn
    board = [""] * 9
    current_turn = "Player"
    for button in buttons:
        button.config(text="", bg="#FFFFFF", activebackground="#D3D3D3")
    result_label.config(text=f"Round {rounds_played + 1} / {max_rounds}")

# Function to display the final result
def display_final_result():
    if player_score > ai_score:
        result_label.config(text=f"Game Over! Player Wins ({player_score} - {ai_score})")
    elif ai_score > player_score:
        result_label.config(text=f"Game Over! AI Wins ({ai_score} - {player_score})")
    else:
        result_label.config(text=f"Game Over! It's a Tie ({player_score} - {ai_score})")

# GUI setup
buttons = []
for i in range(9):
    button = tk.Button(
        root, text="", font=("Helvetica", 24, "bold"),
        width=5, height=2, bg="#FFFFFF", activebackground="#D3D3D3",
        command=lambda i=i: button_click(i)
    )
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

result_label = tk.Label(root, text=f"Round 1 / {max_rounds}", font=("Helvetica", 18), bg="#87CEFA", fg="black")
result_label.grid(row=3, column=0, columnspan=3, pady=20)

# Start the main loop
root.mainloop()
