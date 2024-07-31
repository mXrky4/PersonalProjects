'''
START
    INITIALIZE list_of_passages
    SELECT random_passage from list_of_passages
    PRINT random_passage to screen

    RECORD start_time

    WHILE user_input != random_passage
        READ user_input from user
    END WHILE

    RECORD end_time

    CALCULATE time_taken = end_time - start_time
    CALCULATE accuracy = (number of correct characters / total characters) * 100
    CALCULATE words_per_minute = (number_of_words / time_taken_in_minutes)

    PRINT "Time Taken: " + time_taken
    PRINT "Accuracy: " + accuracy + "%"
    PRINT "Typing Speed: " + words_per_minute + " WPM"

    ASK user if they want to play again
    IF yes
        REPEAT game
    ELSE
        EXIT
END
'''
import tkinter as tk
from tkinter import messagebox
import time
import random

def get_passages():
    return [ "We're no strangers to love",
            "You know the rules and so do I", 
            "A full commitment's what I'm thinking of", 
            "You wouldn't get this from any other guy",
            "I just wanna tell you how I'm feeling",
            "Gotta make you understand",
            "Never gonna give you up" , 
            "Never gonna let you down", 
            "Never gonna run around and desert you"]

def calculate_accuracy(user_input, passage):
    correct_chars = sum(1 for u, p in zip(user_input, passage) if u == p)
    return (correct_chars / len(passage)) * 100

def calculate_accuracy(user_input, passage):
    correct_chars = sum(1 for u, p in zip(user_input, passage) if u == p)
    return (correct_chars / len(passage)) * 100

def start_typing_game():
    global passage, start_time, timer_running
    passage = random.choice(get_passages())
    passage_label.config(text="Type the following passage as quickly as you can:")
    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    passage_text.insert(tk.END, passage)
    passage_text.config(state=tk.DISABLED)
    user_input.delete(0, tk.END)
    user_input.focus()
    start_time = time.time()
    timer_running = True
    update_timer()

def check_typing(event=None):
    global timer_running
    if timer_running:
        user_text = user_input.get()
    if user_text == passage:
        timer_running = False  # Stop the timer
        end_time = time.time()
        time_taken = end_time - start_time
        accuracy = calculate_accuracy(user_text, passage)
        words_per_minute = (len(user_text.split()) / (time_taken / 60)) if time_taken > 0 else 0
        
        result = (f"Time Taken: {time_taken:.2f} seconds\n"
                  f"Accuracy: {accuracy:.2f}%\n"
                  f"Typing Speed: {words_per_minute:.2f} WPM")
        
         # Save the result to the game records
        game_records.append({
                'time_taken': time_taken,
                'accuracy': accuracy,
                'words_per_minute': words_per_minute})

    
        messagebox.showinfo("Results", result)
        replay = messagebox.askyesno("Play Again", "Do you want to play again?")
        if replay:
                start_typing_game()
        else:
                root.quit()
    else:
            # Show an error message and reset the input field
            messagebox.showwarning("Typing Error", "The text does not match. Please try again!")
            user_input.delete(0, tk.END)  # Clear the text entry field
            user_input.focus()  # Refocus on the text entry field

def update_timer():
    if timer_running:
        elapsed_time = time.time() - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        timer_label.config(text=f"Time Elapsed: {minutes:02}:{seconds:02}")
        root.after(1000, update_timer)  # Update the timer every second

def stop_timer():
    global timer_running
    timer_running = False

def show_records():
    if game_records:
        records_text = "Game Records:\n\n"
        for i, record in enumerate(game_records):
            records_text += (f"Game {i+1}:\n"
                             f"Time Taken: {record['time_taken']:.2f} seconds\n"
                             f"Accuracy: {record['accuracy']:.2f}%\n"
                             f"Typing Speed: {record['words_per_minute']:.2f} WPM\n\n")
        records_text = records_text.strip()
    else:
        records_text = "No records available."
    
    messagebox.showinfo("Game Records", records_text)

# Initialize global variables
game_records = []
timer_running = False



root = tk.Tk()
root.title("Typeracer Game")

# Widgets
passage_label = tk.Label(root, text="", wraplength=400)
passage_label.pack(pady=10)

passage_text = tk.Text(root, height=4, width=50, wrap=tk.WORD, state=tk.DISABLED)
passage_text.pack(pady=10)

user_input = tk.Entry(root, width=50)
user_input.pack(pady=10)

check_button = tk.Button(root, text="Finish", command=check_typing)
check_button.pack(pady=10)

start_button = tk.Button(root, text="Start Game", command=start_typing_game)
start_button.pack(pady=10)

timer_label = tk.Label(root, text="Time Elapsed: 00:00")
timer_label.pack(pady=10)

# Bind the "Enter" key to the check_typing function
user_input.bind("<Return>", check_typing)

root.mainloop()