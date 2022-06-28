import random
import pygame
import button

pygame.init()

size = width, height = 500, 300

# Create a screen
screen = pygame.display.set_mode(size)

# Create Background
background = pygame.image.load("BK.jpeg")

# Load objects/options
rock = pygame.image.load("stone.png")
paper = pygame.image.load("paper.png")
cut = pygame.image.load("scissors.png")

# Create button instances
rock_b = button.Button(50, 100, rock, 1)
paper_b = button.Button(200, 100, paper, 1)
cut_b = button.Button(350, 100, cut, 1)

# Surface
surface = pygame.display.get_surface()

# Font
font = pygame.font.Font('freesansbold.ttf', 32)

welcome_font = pygame.font.Font('freesansbold.ttf', 20)

score = 0
num_games = 3
user_choice = ""
comp_choice = "R"
# Intialize random number generator with system time
random.seed()
# Definitions
game = ['R', 'P', 'S']
winner = 0
w = 0
lost = 0
t = 0


# function that prints the current score of the game when called upon
def print_score(x, y):
    print("The current score is ", x, " to ", y, ".")


# add something to check for invalid input: input checking
# figure out what other features can be added to the game


# Intialize random number generator with system time
random.seed()

# Definitions
game = ['R', 'P', 'S']
winner = 0
w = 0
lost = 0
t = 0
score = 0
print("Welcome to the Rock, Paper, Scissors game")
print("How many games would like the match to be best out of?")
num_games = int(input())

# Loop for the game
while score < num_games:
    print("Choose R, P, or S")
    user_choice = input()

    while user_choice not in ['R', 'P', 'S']:
        print("You've failed to follow basic instructions. Try again.")
        user_choice = input()

        # Randomly choose a option for the computer
    comp_choice = random.choice(game)

        # Compare generated option to user input to determine the winner
        # R > S
        # P > R
        # S > P

    if (user_choice == 'R' and comp_choice == 'P') or (user_choice == 'P' and comp_choice == 'S') or (
            user_choice == 'S' or comp_choice == 'R'):
        print('The you chose ' + user_choice)
        print('The computer chose ' + comp_choice)
        print("You lost to a machine!")
        lost += 1
        score += 1
        print_score(w, lost)
        # elif comp_choice == 'S':
        #     print('The you chose ' + user_choice)
        #     print('The computer chose ' + comp_choice)
        #     print("You won!")
        #     w += 1
        #     score += 1
        #     print_score(w, lost)
    # if user_choice == 'P':
    #     if comp_choice == 'S':
    #         print('The you chose ' + user_choice)
    #         print('The computer chose ' + comp_choice)
    #         print("You lost to a machine!")
    #         lost += 1
    #         score += 1
    #         print_score(w, lost)
    elif (user_choice == 'P' and comp_choice == 'R') or (user_choice == 'S' and comp_choice == 'P') or (
            user_choice == 'R' and comp_choice == 'S'):
        print('The you chose ' + user_choice)
        print('The computer chose ' + comp_choice)
        print("You won!")
        w += 1
        score += 1
        print_score(w, lost)

    # if user_choice == 'S':
    # if comp_choice == 'R':
    #     print('The you chose ' + user_choice)
    #     print('The computer chose ' + comp_choice)
    #     print("You lost to a machine!")
    #     lost += 1
    #     score += 1
    #     print_score(w, lost)
    # elif comp_choice == 'P':
    #     print('The you chose ' + user_choice)
    #     print('The computer chose ' + comp_choice)
    #     print("You won!")
    #     w += 1
    #     score += 1
    #     print_score(w, lost)
    elif user_choice == comp_choice:
        print('The you chose ' + user_choice)
        print('The computer chose ' + comp_choice)
        print("Try again!")
        t += 1
        print_score(w, lost)

print("You won: ", w, "times ")
print("You lost: ", lost, "times")
print("You tied: ", t, "times")
if w < lost:
    print("SHAME ON YOU!!")

print("Thank you for playing")
