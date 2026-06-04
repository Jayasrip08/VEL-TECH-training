# number guessing game 

import random
def check_guess(secret, guess):
    if guess == secret:
        return "Correct! 🎉"
    elif guess < secret:
        return "Too low! Try higher"
    else:
        return "Too high! Try lower"

secret = random.randint(1, 10)

for attempt in range(3):
    guess = int(input("Guess: "))
    print(check_guess(secret, guess))
