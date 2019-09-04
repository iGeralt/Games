import random
num = random.randint(1,100)
print("\t\t\tWelcome to the GUESS GAME\n")
print("Choose a number between 1 and 100")
print("If your number is more than 10 away from my number then you are Good ")
print("If your number is within 10 of my number then you are smart")
print("If your number is closer than your previously guessed number then you are getting closer to number")
print("If your number is farther than your previously guessed number then you are getting away from number\n\n")
print("\t\t\tLet's play the game")
total_guess = [0]
while True:

    guess = int(input("Guess the number : "))

    if guess < 1 or guess > 100:
        print("You have to choose number between 1 and 100")
        continue

    if guess == num:
        print("\n\t\t\tYou won.You took {g} guesses!!".format(g = len(total_guess)))
        break
    total_guess.append(guess)

    if total_guess[-2]:
        if abs(guess - num) > abs(total_guess[-2] - num):
            print("You are getting away from number!!\n")
        else:
            print("You are getting closer to the number!!\n")

    else:
        if abs(guess - num) >= 10:
            print("You are Good!!\n")
        else:
            print("You are Smart!!\n")
