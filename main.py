import tkinter as tk
from tkinter import messagebox
from ttkbootstrap import Style

# defining a variable
WORD_LENGTH = 5


def checkGuessValid(current_word: str, colours: str, guess_word: str) -> bool:
    """
    This function takes in the current word inputted into wordle, the colours outputted,
    and some guess word.

    It checks if the guess word is a valid guess given the current word and its letter colours.

    Checks all current_word green letters first, and replaces their in-place occurrence in
    the guess with a dash. Otherwise, returns false

    Then checks all current_word yellow letters, and replaces their first out-of-place occurrence
    in the guess with a dash. Otherwise, returns false

    Then checks all current_word black letters, return false if any occurrences still left
    in the guess word

    Otherwise, return true
    """
    guess_mod: str = guess_word
    for i in range(WORD_LENGTH):
        if colours[i] == 'g':
            if guess_word[i] != current_word[i]:
                return False
            else:
                guess_mod = guess_mod[:i] + '-' + (guess_mod[i + 1:] if i + 1 < WORD_LENGTH else '')

    for i in range(WORD_LENGTH):
        if colours[i] == 'y':
            if current_word[i] not in guess_mod or guess_mod[i] == current_word[i]:
                return False
            else:
                k = guess_mod.find(current_word[i])
                guess_mod = guess_mod[:k] + '-' + (guess_mod[k + 1:] if k + 1 < WORD_LENGTH else '')

    for i in range(WORD_LENGTH):
        if colours[i] == 'b':
            if current_word[i] in guess_mod:
                return False

    return True


def pickRandomWord(word_list) -> str:
    alphabet_dict = {char: 0 for char in 'abcdefghijklmnopqrstuvwxyz'}

    for word in word_list:
        for char in word:
            if char in alphabet_dict:
                alphabet_dict[char] += 1

    word_scores = {}

    for word in word_list:
        score = sum([alphabet_dict[char] for char in word])
        word_scores[word] = score

    def repeated_letters(w):
        """Return the number of repeated letters in a word."""
        return len(w) - len(set(w))

    # Progressively allow repeated letters
    threshold = 0
    filtered_words = []

    while not filtered_words and threshold <= len(word_list[0]):
        filtered_words = [word for word in word_list if repeated_letters(word) <= threshold]
        threshold += 1

    # Sort the filtered words by score
    sorted_filtered_words = sorted(filtered_words, key=lambda x: word_scores[x], reverse=True)

    # The word with the highest score from the filtered list
    return sorted_filtered_words[0]

def check_result(event=None):
    global word_list, current_word

    user_input = input_entry.get().strip()
    if len(user_input) != 5 or any(c not in 'gyb' for c in user_input):
        messagebox.showerror("Invalid Input", "Please enter a valid 5-character input using 'g', 'y', or 'b'.")
        input_entry.delete(0, 'end')
    else:
        valid_words = [word for word in word_list if checkGuessValid(current_word, user_input, word)]
        if len(valid_words) < 1:
            messagebox.showinfo("Game Over", "There are no valid words left. Something went wrong!")
            window.destroy()
        else:
            word_list.clear()
            word_list.extend(valid_words)
            current_word = pickRandomWord(word_list)
            guess_label.config(text=f"Next guess: {current_word}")
            input_entry.delete(0, 'end')

# Create the main GUI window
window = tk.Tk()
window.title("Wordle Solver")

# Create a custom style for the GUI elements using ttkbootstrap
style = Style(theme="yeti")  # You can choose different themes

# Create and set up GUI elements with padding and styles
container = tk.Frame(window, padx=20, pady=20)
container.pack()

guess_label = tk.Label(container, text="Next guess: ")
style.configure("TLabel", background=style.colors.primary, foreground="white")
guess_label.pack()

input_label = tk.Label(container, text="Enter result (gybbb):")
style.configure("TLabel", background=style.colors.primary, foreground="white")
input_label.pack()

input_entry = tk.Entry(container, font=("Arial", 12))
style.configure("TEntry", padding=10, bordercolor=style.colors.secondary)
input_entry.pack()

submit_button = tk.Button(container, text="Submit", command=check_result)
style.configure("TButton", padding=10, font=("Arial", 12))
submit_button.pack()

# Bind the Enter key to the Submit button
input_entry.bind('<Return>', check_result)

# Initialize the game
word_list = []
with open('words.txt', 'r') as file:
    for line in file:
        line = line.strip()
        word_list.append(line)
current_word = pickRandomWord(word_list)
guess_label.config(text=f"Next guess: {current_word}")

# Start the GUI main loop
window.mainloop()