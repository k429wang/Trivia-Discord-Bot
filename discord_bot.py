import random, requests, sys, discord

# TODO
# - implement answer detection (use same message detection function or make new one or implement into a def function)
# - timer for answers
# - permanent stats for users
# - find a server to run the bot in the cloud 24/7?

token = open('token.txt', 'r')
TOKEN = token.read()

client = discord.Client()

url = 'https://opentdb.com/api.php?amount=10'
amount = 10
category = 0
difficulty = 0 
qtype = 0
answering_state = False
counter = 0
user_list = []

def update_url():
    global url
    url = 'https://opentdb.com/api.php?amount=' + str(amount) + '&category=' + str(category) + '&difficulty=' + str(difficulty) + '&type=' + str(qtype)
        
@client.event
async def on_ready():
    print('Logged in with {0.user}'.format(client))

@client.event
async def on_message(message):
    global counter

    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    print(f'{username}: {user_message}')

    if ((username in user_list)==False):
        user_list.append(username)
        if ('TriviaBot' in user_list):
            user_list.remove('TriviaBot')

    if message.author == client.user:
        return

    match user_message:
        case '$tryhard check':
            x = random.randint(0,3)
            user = random.choice(user_list)
            match x:
                case 0:
                    await message.channel.send(user + " is tryharding 24/7.")
                case 1:
                    await message.channel.send("Stop " + user + " from tryharding!!")
                case 2:
                    await message.channel.send(user + " is literally the sweatiest tryhard in the universe")
                case 3:
                    await message.channel.send(user + " never tryhards")
            return
        case '$help':
            await message.channel.send('''
This is a Trivia bot made by Kai Wang using the OpenTrivia database. Available commands:
    $start -> Begin playing
    $settings -> Change the game settings
    $quit -> Stop the current game
    $tryhard check -> ;)
''')
            return
        case '$start':
            update_url()

            response = requests.get(url)
            trivia = response.json()
            results = trivia['results']

            if (counter < amount):

                question = results[counter]

                await message.channel.send(question['question'])

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

                    await message.channel.send(f'''
A: {answers[0]}
B: {answers[1]}
C: {answers[2]}
D: {answers[3]}
''')
                elif(question['type'] == 'boolean'):
                    await message.channel.send('True OR False?')

                counter += 1
    
if __name__ == '__main__':
    client.run(TOKEN)