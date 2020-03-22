from discord.ext import commands
from random import randint

TOKEN = 'NjkxMDIyNjg0NDk0MTAyNTM5.XndEBQ.8BT1awboOl6roSj_RW0DPX62Fa0'
client = commands.Bot(command_prefix='master ')

@client.event
async def on_ready():
    print('Bot is Ready.')
    
@client.command()
async def scelgo(ctx, name):
    channel = ctx.channel
    if channel.name == 'lupi':
        await ctx.send(f'Avete scelto {name}, domani mattina morirà.')
    else:
        await ctx.send('Voi non siete lupi...')


# Il codice qui sotto rimprovera chi dice le parolacce
bad_words_file = open('bad_words.txt', 'r')
content = bad_words_file.read()
bad_words = set(content.split())

@client.event
async def on_message(message):
    author = message.author
    channel = message.channel
    content = message.content
    if author.bot:
        return
    
    # Sceglie l'epiteto di genere in modo casuale
    epiteto = 'bello' if randint(0, 1) == 0 else 'bella'
    word_list = content.split()
    for word in word_list:
        if word in bad_words:
            stars = '**' + '\*' * (len(word) - 2) + '**'
            censored = word[:1] + stars + word[-1:]
            answer = f'Non si dice {censored}, {epiteto}!'
            await channel.send(answer)

client.run(TOKEN)

