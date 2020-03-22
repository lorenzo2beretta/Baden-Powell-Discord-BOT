import random
from discord.ext import commands, tasks

TOKEN = 'NjkxMDIyNjg0NDk0MTAyNTM5.XndW5Q.T-gHo8bzEW0ka7qlh_6O4aIt_NQ'
bot = commands.Bot(command_prefix=['bp ', 'BP ', 'B.P. ', 'b.p. '])
bot.case_insensitive = True

@bot.event
async def on_ready():
    print('Bot is Ready.')

# Questo comando fornisce citazioni di BP quando richiesto
bp_quotes_file = open('bp_quotes.txt', 'r')
quotes = bp_quotes_file.readlines()
quotes = ['"' + quote[:-1] + '"' for quote in quotes]
bp_quotes_file.close()

@bot.command()
async def citazione(ctx):
    channel = ctx.channel
    epiteto = random.choice(['mio caro', 'mia cara'])
    intro = f'Eccoti una mia bellissima citazione, {epiteto}!\n'
    quote = random.choice(quotes)
    await channel.send(intro + quote)

# Il codice qui sotto rimprovera chi dice le parolacce
bad_words_file = open('bad_words.txt', 'r')
content = bad_words_file.read()
bad_words = sorted(content.split(), key=lambda s: len(s), reverse=True)
bad_words_file.close()

@bot.event
async def on_message(message):
    # waits commands to be processed
    await bot.process_commands(message)
    author = message.author
    channel = message.channel
    content = message.content
    if author.bot:
        return
    
    # Sceglie l'epiteto di genere in modo casuale
    epiteto = random.choice(['bello', 'bella'])
    word_list = ''.join(content.split())
    for word in bad_words:
        if word in word_list:
            stars = '**' + '\*' * (len(word) - 2) + '**'
            censored = word[:1] + stars + word[-1:]
            answer = f'Non si dice {censored}, {epiteto}!'
            await channel.send(answer)
            break

bot.run(TOKEN)

