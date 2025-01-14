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
import pygame

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

def start_typing_game():
    global passage, start_time, timer_running
    passage = random.choice(get_passages())
    passage_label.config(text="Type the following passage as quickly as you can:")

    # Set the passage text in grey
    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    passage_text.insert(tk.END, passage)
    passage_text.tag_configure('grey', foreground='grey')
    passage_text.tag_add('grey', '1.0', tk.END)
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

         # Display all records
        show_records()

        

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

def show_records():
    if game_records:
        records_text = "Game Records:\n\n"
        total_wpm = 0
        for i, record in enumerate(game_records):
            records_text += (f"Game {i+1}:\n"
                             f"Time Taken: {record['time_taken']:.2f} seconds\n"
                             f"Accuracy: {record['accuracy']:.2f}%\n"
                             f"Typing Speed: {record['words_per_minute']:.2f} WPM\n\n")
            total_wpm += record['words_per_minute']
        
        average_wpm = total_wpm / len(game_records) if game_records else 0
        records_text += (f"Average WPM: {average_wpm:.2f}")
        records_text = records_text.strip()
    else:
        records_text = "No records available."
    
    messagebox.showinfo("Game Records", records_text)

def on_type(event=None):
    user_text = user_input.get()
    display_passage = passage

    # Set all text to grey
    passage_text.config(state=tk.NORMAL)
    passage_text.delete(1.0, tk.END)
    passage_text.insert(tk.END, display_passage)
    passage_text.tag_configure('grey', foreground='grey')
    passage_text.tag_add('grey', '1.0', tk.END)

    # Check the user input and update text color
    for i, char in enumerate(user_text):
        if i < len(passage):
            if char == passage[i]:
                passage_text.tag_add('black', f"1.{i}", f"1.{i+1}")
                passage_text.tag_configure('black', foreground='black')
            else:
                passage_text.tag_configure('grey', foreground='grey')
                
    passage_text.config(state=tk.DISABLED)

def play_music():
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("Pure Imagination - Lofi Cover.mp3")  # Replace with your music file
        pygame.mixer.music.set_volume(0.2)  # Set volume (0.0 to 1.0)
        pygame.mixer.music.play(-1)  # Loop the music indefinitely
    except pygame.error as e:
        print(f"Error loading music: {e}")

# Initialize global variables
game_records = []
timer_running = False



root = tk.Tk()
root.title("Typeracer Game")

# Set the size of the window
root.geometry("800x600")  # Width x Height

# Widgets
passage_label = tk.Label(root, text="", wraplength=780, font=("Arial", 16) )
passage_label.pack(pady=20)

passage_text = tk.Text(root, height=6, width=80, wrap=tk.WORD, state=tk.DISABLED, font=('Arial', 16))
passage_text.pack(pady=20)

user_input = tk.Entry(root, width=80, font=('Arial', 16))
user_input.pack(pady=20)

instructions_label = tk.Label(root, text="Press Enter when you finish typing", font=("Arial", 14))
instructions_label.pack(pady=10)

start_button = tk.Button(root, text="Start Game", command=start_typing_game, font=('Arial', 16))
start_button.pack(pady=20)

timer_label = tk.Label(root, text="Time Elapsed: 00:00", font=('Arial', 16))
timer_label.pack(pady=20)

# Bind the "Enter" key to the check_typing function
user_input.bind("<Return>", check_typing)

# Bind the typing event to update the passage color
user_input.bind("<KeyRelease>", on_type)

#play background music
play_music()

root.mainloop()