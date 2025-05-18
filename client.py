import random, requests, asyncio, discord

# TODO
# - fix json parsing issue
# - permanent stats for users
# - add answer streak feature
# - find a server to run the bot in the cloud 24/7?
# - implement 'settings' feature

# Initialize client side discord API using TOKEN
token = open('token.txt', 'r')
TOKEN = token.read()
client = discord.Client()

# Updates the trivia database API call
def update_url():
    global url
    url = 'https://opentdb.com/api.php?amount=' + str(amount) + '&category=' + str(category) + '&difficulty=' + str(difficulty) + '&type=' + str(qtype)

# Called by '$start' command -> starts printing questions to the console
async def print_question(message):
    global answering_state, url, counter, question, correct_players

    update_url()

    # Getting data from Open Trivia DataBase using their API url
    response = requests.get(url)
    trivia = response.json()
    results = trivia['results']

    for x in range(int(amount)):
        if (answering_state==True):

            question = results[x]

            # Sends the question into the channel as a message
            await message.channel.send(f'''
----------------------------------------
{question['question']}
''')

            # Sends multiple choice options into the channel as a message
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
                await asyncio.sleep(10)
                for x in players_dic:
                    if ((players_dic[x].capitalize() in answers_dic)and(answers_dic[players_dic[x].capitalize()]==question['correct_answer'])):
                        correct_players.append(x)
                await message.channel.send('The answer is: '+question['correct_answer'])
                await message.channel.send(f'''
Congratulations: 
{correct_players}
''')
            # Sends true or false query into the channel as a message
            elif(question['type'] == 'boolean'):
                await message.channel.send('True OR False?')
                await asyncio.sleep(10)
                for x in players_dic:
                    if (players_dic[x].capitalize()==question['correct_answer']):
                        correct_players.append(x)
                await message.channel.send('The answer is: '+question['correct_answer'])
                await message.channel.send(f'''
Congratulations: 
{correct_players}
''')
            correct_players.clear()
            players_dic.clear()
            await asyncio.sleep(3)
    await message.channel.send('Game over! Thanks for playing.')
    answering_state = False

# Prints a message when the bot is connected
@client.event
async def on_ready():
    print('Logged in with {0.user}'.format(client))

# Triggers when a message is sent in the discord server
@client.event
async def on_message(message):
    global counter, answering_state, question, answers_dic, players_dic

    # Keep track of all the messages in the bot channel
    username = str(message.author).split('#')[0]
    user_message = str(message.content)
    print(f'{username}: {user_message}')

    # Make sure bot does not interact with itself
    if message.author == client.user:
        return

    # Add new users to user list & make sure the bot is not in the list
    if ((username in user_list)==False):
        user_list.append(username)

    # Respond to commands in discord server
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
        case '$help':
            await message.channel.send('''
This is a Trivia bot made by Kai Wang using the OpenTrivia database. Available commands:
    $start -> Begin playing
    $settings -> Change the game settings
    $stop -> Stop the current game
    $tryhard check -> :)
''')
        case '$start':
            if (answering_state == False):
                answering_state = True
                await print_question(message)
            elif (answering_state == True):
                await message.channel.send("Existing game is already running. Enter $stop to terminate.")
        case '$stop':
            answering_state = False
            await message.channel.send("Game terminated")
        case _:
            if (answering_state == True):
                players_dic[username] = user_message
                
def main():
    client.run(TOKEN)

# Main function to declare variables and run discord client
if __name__ == '__main__':
    url = 'https://opentdb.com/api.php?amount=10'
    amount = 10
    category = 0
    difficulty = 0 
    qtype = 0
    answering_state = False
    counter = 0
    user_list = []
    question = ''
    answers_dic = {}
    players_dic = {}
    correct_players = []

    main()