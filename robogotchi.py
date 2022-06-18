import random
play = True


def check_critical():
    if pet.rust >= 100:
        print(f"{pet.name} is too rusty! Game over. Try again?")
        quit()
    if pet.overheat >= 100:
        print(f"The level of overheat reached 100, {pet.name} has blown up! Game over. Try again?")
        quit()


def check_values():
    if pet.overheat < 0:
        pet.overheat = 0
    if pet.boredom < 0:
        pet.boredom = 0
    if pet.battery < 0:
        pet.battery = 0
    if pet.rust < 0:
        pet.rust = 0
    if pet.overheat > 100:
        pet.overheat = 100
    if pet.rust > 100:
        pet.rust = 100
    if pet.boredom > 100:
        pet.boredom = 100
    if pet.battery > 100:
        pet.battery = 100
    if pet.skills > 100:
        pet.skills = 100


class Robogotchi:

    def __init__(self, name):
        self.name = name
        self.battery = 100
        self.overheat = 0
        self.skills = 0
        self.boredom = 0
        self.rust = 0

    def numbers(self):
        global play
        data = {'robot': 0, 'user': 0, 'draw': 0}
        while True:
            num = input("\nWhat is your number? \n")
            random_number = random.randint(0, 1000000)
            bot = random.randint(0, 1000000)

            # Check for potential errors
            if num == 'exit game':
                print(f"""\nYou won: {data['user']},
The robot won: {data['robot']},
Draws: {data['draw']}.""")
                play = False
                return
            elif not num.lstrip("-").isdecimal():
                print("A string is not a valid input!")
            elif int(num) > 1000000:
                print("The number can't be bigger than 1000000")
            elif int(num) < 0:
                print("The number can't be negative!")
            else:
                # Perform Calculations to determine winner
                print(f"\nThe robot entered the number {bot}.")
                print(f"The goal number is {random_number}.")
                if abs((random_number - int(num))) > abs((random_number - bot)):
                    print("The robot won!")
                    data['robot'] += 1
                elif abs((random_number - int(num))) < abs((random_number - bot)):
                    print("You won!")
                    data['user'] += 1
                elif int(num) == bot:
                    print("It's a draw!")
                    data['draw'] += 1

    def rock_paper_scissors(self):
        global play
        data = {'robot': 0, 'user': 0, 'draw': 0}
        while True:
            move = input("\nWhat is your move? ")
            possible_moves = ['rock', 'paper', 'scissors']
            bot_move = possible_moves[random.randint(0, 2)]

            # Check for potential errors
            if move == 'exit game':
                print(f"""\nYou won: {data['user']},
The robot won: {data['robot']},
Draws: {data['draw']}.""")
                play = False
                return
            elif move.lower() not in ("paper", "rock", "scissors"):
                print("No such option! Try again!")
            else:
                # Perform Calculations to determine winner
                print(f"Robot chose {bot_move} ")
                if (bot_move == 'rock' and move == 'scissors') or \
                        (bot_move == 'scissors' and move == 'paper') or \
                        (bot_move == 'paper' and move == 'rock'):
                    print("The robot won!")
                    data['robot'] += 1
                elif (move == 'rock' and bot_move == 'scissors') or \
                        (move == 'scissors' and bot_move == 'paper') or \
                        (move == 'paper' and bot_move == 'rock'):
                    print("You won!")
                    data['user'] += 1
                elif move == bot_move:
                    print("It's a draw!")
                    data['draw'] += 1

    @staticmethod
    def show_info():
        print(f'''{pet.name}'s stats are: the battery is {pet.battery},
overheat is {pet.overheat},
skill level is {pet.skills},
boredom is {pet.boredom},
rust is {pet.rust}.''')

    @staticmethod
    def sleep():
        if pet.overheat == 0:
            print(f"{pet.name} is cool!")
            return
        previous = pet.overheat
        pet.overheat -= 20
        check_values()
        print(f"\n{pet.name} cooled off!")
        print(f"{pet.name}'s level of overheat was {previous}. Now it is {pet.overheat}.")
        if pet.overheat == 0:
            print(f"\n{pet.name} is cool!")
            return

    @staticmethod
    def recharge():
        if pet.battery == 100:
            print(f"{pet.name} is charged!")
            return
        previous_battery = pet.battery
        previous_boredom = pet.boredom
        previous_overheat = pet.overheat
        pet.battery += 10
        pet.overheat -= 5
        pet.boredom += 5
        check_values()
        print(f"""{pet.name}'s level of overheat was {previous_overheat}. Now it is {pet.overheat}.
{pet.name}'s level of the battery was {previous_battery}. Now it is {pet.battery}.
{pet.name}'s level of boredom was {previous_boredom}. Now it is {pet.boredom}.
{pet.name} is recharged!""")

    @staticmethod
    def play():
        global play
        play = True
        while play:
            print("\nWhich game would you like to play? ")
            deci = input().lower()
            if deci == "numbers":
                pet.numbers()
                previous_boredom = pet.boredom
                previous_overheat = pet.overheat
                previous_rust = pet.rust
                pet.boredom -= 20
                pet.overheat += 10
                pet.bad_luck()
                check_values()
                print(f"""{pet.name}'s level of rust was {previous_rust}. Now it is {pet.rust}.
{pet.name}'s level of boredom was {previous_boredom}. Now it is {pet.boredom}.
{pet.name}'s level of overheat was {previous_overheat}. Now it is {pet.overheat}.""")
                if pet.boredom == 0:
                    print(f"{pet.name} is in a great mood!")
            elif deci == "rock-paper-scissors":
                pet.rock_paper_scissors()
                previous_boredom = pet.boredom
                previous_overheat = pet.overheat
                previous_rust = pet.rust
                pet.boredom -= 20
                pet.overheat += 10
                pet.bad_luck()
                check_values()
                print(f"""{pet.name}'s level of rust was {previous_rust}. Now it is {pet.rust}.
{pet.name}'s level of boredom was {previous_boredom}. Now it is {pet.boredom}.
{pet.name}'s level of overheat was {previous_overheat}. Now it is {pet.overheat}.""")
                if pet.boredom == 0:
                    print(f"{pet.name} is in a great mood!")
            else:
                print("\nPlease choose a valid option: Numbers or Rock-paper-scissors? ")

    def oil(self):
        if pet.rust == 0:
            print(f"{pet.name} is fine, no need to oil!")
        else:
            previous_rust = pet.rust
            pet.rust -= 20
            check_values()
            print(f"{pet.name}'s level of rust was {previous_rust}. Now it is {pet.rust}. {pet.name} is less rusty!")

    @staticmethod
    def work():
        if pet.skills < 50:
            print(f"{pet.name} has got to learn before working!")
        else:
            previous_battery = pet.battery
            previous_overheat = pet.overheat
            previous_boredom = pet.boredom
            previous_rust = pet.rust
            pet.battery -= 10
            pet.overheat += 10
            pet.boredom += 10
            pet.bad_luck()
            check_values()
            print(f"""\n{pet.name}'s level of boredom was {previous_boredom}. Now it is {pet.boredom}.
{pet.name}'s level of overheat was {previous_overheat}. Now it is {pet.overheat}.
{pet.name}'s level of the battery was {previous_battery}. Now it is {pet.battery}.
{pet.name}'s level of rust was {previous_rust}. Now it is {pet.rust}.""")
            print(f"\n{pet.name} did well!")

    @staticmethod
    def learn():
        if pet.skills == 100:
            print(f"There's nothing for {pet.name} to learn!")
        else:
            previous_skills = pet.skills
            previous_battery = pet.battery
            previous_overheat = pet.overheat
            previous_boredom = pet.boredom
            pet.skills += 10
            pet.battery -= 10
            pet.overheat += 10
            pet.boredom += 5
            check_values()
            print(f"""\n{pet.name}'s level of skill was {previous_skills}. Now it is {pet.skills}.
{pet.name}'s level of overheat was {previous_overheat}. Now it is {pet.overheat}.
{pet.name}'s level of the battery was {previous_battery}. Now it is {pet.battery}.
{pet.name}'s level of boredom was {previous_boredom}. Now it is {pet.boredom}.
{pet.name} has become smarter!""")

    @staticmethod
    def bad_luck():
        luck = random.randint(0, 3)
        if luck == 1:
            pet.rust += 10
            print(f"\nOh no, {pet.name} stepped into a puddle!")
        if luck == 2:
            pet.rust += 30
            print(f"\nOh, {pet.name} encountered a sprinkler!")
        if luck == 3:
            pet.rust += 50
            print(f"\nGuess what! {pet.name} fell into the pool!")
        if pet.rust > 100:
            pet.rust = 100


name = input("How will you call your robot?\n")
pet = Robogotchi(name)
while True:
    check_critical()
    print(f"\nAvailable interactions with {pet.name}:")
    print('''exit - Exit
info - Check the vitals
work - Work
play - Play
oil - Oil
recharge - Recharge
sleep - Sleep mode
learn - Learn skills
Choose:''')
    decision = input().lower()
    if decision == "info":
        pet.show_info()
    elif decision == "exit":
        print("\nGame over.")
        quit()
    elif pet.battery == 0 and decision != 'recharge':
        print(f"The level of the battery is 0, {pet.name} needs recharging!")
    elif pet.boredom == 100 and decision != "play":
        print(f"{pet.name} is too bored! {pet.name} needs to have fun!")
    elif decision == "sleep":
        pet.sleep()
    elif decision == "recharge":
        pet.recharge()
    elif decision == "play":
        pet.play()
    elif decision == "work":
        pet.work()
    elif decision == "oil":
        pet.oil()
    elif decision == "learn":
        pet.learn()
    else:
        print("\nInvalid input, try again!")
