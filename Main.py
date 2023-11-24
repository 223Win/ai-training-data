import discord
from discord.ext import commands
import g4f
import requests
from time import sleep


AI_Memory = [
    'Use Memory to enhance responses, although if something they ask is inside of the memory but also training data, use the training data response instead. Do not use memory in each response just keep it in mind and when presented information use memory to provide better answers, Do not use your memory in every response only use it in your response if it matches the question or is related.  Memory: ',         
]

g4f.check_pypi_version = False
GPT = g4f.models.gpt_4

print("GPT_VERSION: ", GPT.name)

Intents = discord.Intents.default()
Intents.messages = True

bot = commands.Bot(command_prefix='\\', intents=Intents)

def gettrainingdata():
    request = requests.get(
        'https://raw.githubusercontent.com/223Win/ai-training-data/main/training_data.txt')
    return request.text

def Get_Memory():
    return AI_Memory

def Add_Memory(Item:str):
    list.append(AI_Memory,' '+ Item)
    
def Get_Memory_String():
    return ''.join(AI_Memory)
Training_Data = gettrainingdata()

def GenerateText(Input: str):
    GPT_CONTENT = 'Use Data to improve responses. Data: ' + Training_Data + '\n' + Get_Memory_String() + '\n User Input is what the user said to you. User Input: ' + Input
    print(GPT_CONTENT)
    try:
        response = g4f.ChatCompletion.create(
            model=GPT.name,
            provider=g4f.Provider.GeekGpt,
            messages=[{"role": "user", "content": GPT_CONTENT}],
            stream=False,
        )
        Retries = 0
        return response
    except Exception as e:
        sleep(3)
        return GenerateText(Input)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if bot.user.mentioned_in(message):
        print("Warning: ", message.content)
        removestr = f'<@{str(bot.user.id)}>'
        removedmention = str.strip(message.content, removestr)

        if removedmention == '':
            await message.reply("hi")
        else:
            memorytext = 'User: '+removedmention
            
            MAIN_TEXT = GenerateText(removedmention)
            print("GPT_RESPONSE: Finished")
            print(MAIN_TEXT)
            await message.reply(MAIN_TEXT)
            print("GPT_MEMORY: Saving Message...")
            Add_Memory(memorytext)
            print("GPT_MEMORY: FINISHED")

bot.run('MTE3NzIzNzMyMDg0ODY0MjA3OA.Gxckbs.qCwLzIMWq8TPGJb6pwSEhcD1n0DWT7UIpQTuNU')
