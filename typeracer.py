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
import time
import random

def get_passages():
    return [ "We're no strangers to love.",
            "You know the rules and so do I.", 
            "A full commitment's what I'm thinking of", 
            "You wouldn't get this from any other guy"]

def calculate_accuracy(user_input, passage):
    correct_chars = sum(1 for u, p in zip(user_input, passage) if u == p)
    return (correct_chars / len(passage)) * 100

def typing_game():
    passages = get_passages()
    passage = random.choice(passages)


# display passage
    print("Type the following passage as quickly as you can:")
    print(passage)
   

# capture user input
    start_time = time.time()
    user_input = input("Start typing:")
    end_time = time.time()
    

# calculating speed and accuracy
    time_taken = end_time - start_time
    accuracy = calculate_accuracy(user_input, passage)
    words_per_minute = (len(user_input.split()) / (time_taken / 60)) if time_taken > 0 else 0
    

#display result
    print(f"Time Taken: {time_taken:.2f} seconds")
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Typing Speed: {words_per_minute:.2f} WPM")
    

def main():
    while True:
        typing_game() #to start the game
        replay = input("Do you want to play again? (yes/no): ")
        if replay != "yes":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

