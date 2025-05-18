import random, requests, sys

# TODO
# - fix weird string parsing issue (some characters aren't printing correctly)
# - fix issue where there isn't enough questions so the API just returns empty json file

# Updates the trivia database API call
def update_url():
    global url
    url = 'https://opentdb.com/api.php?amount=' + str(amount) + '&category=' + str(category) + '&difficulty=' + str(difficulty) + '&type=' + str(qtype)

# Called by 'start' command -> starts printing questions to the console
def start():

    # Getting data from Open Trivia DataBase using their API url
    response = requests.get(url)
    trivia = response.json()

    # Writing the data to a JSON file for testing purposes
    # with open ("data.json", "w") as write_file:
    #     json.dump(trivia, write_file)

    # Opening a JSON file for testing purposes
    # with open ("data.json", "r") as read_file:
    #     trivia = json.load(read_file)

    results = trivia['results']

    counter = 0

    # Loop through trivia JSON file to print questions
    for x in range(int(amount)):

        question = results[x]

        print(question['question'])

        if (question['type'] == 'multiple'):
            answers = question['incorrect_answers']
            answers.append(question['correct_answer'])
            random.shuffle(answers)
            answers_dic = {
                'A': answers[0],
                'B': answers[1],
                'C': answers[2],
                'D': answers[3]
                }

            print('A: ' + answers[0])
            print('B: ' + answers[1])
            print('C: ' + answers[2])
            print('D: ' + answers[3])

            x = input()

            if (x.capitalize() in answers_dic)and(answers_dic[x.capitalize()] == question['correct_answer']):
                counter += 1
                print('CORRECT!')
            elif(x == 'quit'):
                quit()
            else:
                counter = 0
                print('INCORRECT. The correct answer is: ' + question['correct_answer'])

        elif(question['type'] == 'boolean'):
            print('True OR False?')

            x = input()

            if (x.capitalize() == question['correct_answer']):
                counter += 1
                print('CORRECT!')
            elif(x == 'quit'):
                quit()
            else:
                counter = 0
                print('INCORRECT. The correct answer is: ' + question['correct_answer'])

        if (counter != 0):
            print("Streak: " + str(counter))

# Called by 'settings' command -> starts printing settings commands to the console
def settings():
    global amount, category, difficulty, qtype

    # Event loop -> Loop through settings commands until user inputs 'done'
    while (True):
        print('What would you like to change? (Options: amount, category, difficulty, type, OR done)')
        x = input()
        match x:
            case 'amount':
                print('Enter the amount of questions you would like to have (max 50):')
                amount = input()
            case 'category':
                print("""
Pick a category:
9 - General Knowledge
10 - Entertainment: Books 
11 - Entertainment: Film 
12 - Entertainment: Music 
13 - Entertainment: Musicals & Theatres 
14 - Entertainment: Television 
15 - Entertainment: Video Games 
16 - Entertainment: Board Games 
17 - Science & Nature 
18 - Science: Computers 
19 - Science: Mathematics 
20 - Mythology 
21 - Sports 
22 - Geography 
23 - History 
24 - Politics
25 - Art 
26 - Celebrities
27 - Animals 
28 - Vehicles 
29 - Entertainment: Comics 
30 - Science: Gadgets
31 - Entertainment: Japanese Anime & Manga 
32 - Entertainment: Cartoon & Animations
                """)
                category = input()
            case 'difficulty':
                print('Enter the difficulty of questions (easy, medium, or hard):')
                difficulty = input()
            case 'type':
                print('What type of questions would you like?')
                print('''
multiple - Multiple Choice
boolean - True or False
0 - Both
''')
                qtype = input()
            case 'done':
                update_url()
                break

# Called by 'quit' command -> exits the program
def quit():
    print("Thank you for playing!")
    sys.exit(0)

# Runs on launch, initializes game and gives user instructions
def run():
    update_url()

    print("This is a Trivia bot made by Kai Wang using the OpenTrivia database.")

    #Event loop -> Loops through game commands until user inputs 'quit'
    while (True):
        print("Enter 'start' to begin playing, 'settings' to access settings, and 'quit' to terminate the program.")
        x = input()
        match x:
            case 'start':
                start()
            case 'settings':
                settings()
            case 'quit':
                quit()
            case _:
                print("Please enter a valid input.")
    
def main():
    run()

# Main function to declare variables and start the game
if __name__ == '__main__':
    # Declare global URL variables
    url = 'https://opentdb.com/api.php?amount=10'
    amount = 10
    category = 0
    difficulty = 0 
    qtype = 0

    main()