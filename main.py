import requests, json, sys

# TODO
# - implement url editing features in settings function(ex. choosing categories, difficulties, question types, etc.)
# - figure out how to display possible answers in a random order
# - fix weird string parsing issue (some characters aren't printing correctly)
# - implement into discord bot and/or website (website will need a gui)


def start():

    # Getting data from Open Trivia DataBase using their API url
    response = requests.get('https://opentdb.com/api.php?amount=10')
    trivia = response.json()

    # Writing the data to a JSON file for testing purposes
    # with open ("data.json", "w") as write_file:
    #     json.dump(trivia, write_file)

    # Opening a JSON file for testing purposes
    # with open ("data.json", "r") as read_file:
    #     trivia = json.load(read_file)

    results = trivia['results']

    question = results[0]

    print(question['question'])

    x = input()

    if (x == question['correct_answer']):
        print('Correct!')
    else:
        print('Incorrect. The correct answer is: ' + question['correct_answer'])

def settings():
    print('settings')

def quit():
    print("Thank you for playing!")
    sys.exit(0)

def run():
    print("This is a Trivia bot made by Kai Wang using the OpenTrivia database.")

    while (True):
        print("Enter 'start' to begin playing, 'settings' to access settings, and 'quit' to terminate the program.")
        x = input()
        if (x == 'start'):
            start()
        elif(x == 'settings'):
            settings()
        elif(x == "quit"):
            quit()
        else:
            print("Please enter a valid input.")
    

if __name__ == '__main__':
    run()