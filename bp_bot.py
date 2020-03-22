import random
import schedule
import discord
from discord.ext import commands, tasks

TOKEN = 'NjkxMDIyNjg0NDk0MTAyNTM5.XndzZw.057cZ_GJmFKP4Igp2SPosI_cqZo'
GENERAL_CHAT = 691024389730336842
bot = commands.Bot(command_prefix=['bp ', 'BP ', 'B.P. ', 'b.p. '])

@bot.event
async def on_ready():
    print('Bot is Ready.')
    
@tasks.loop(hours=24, count=5)
async def count():
    await bot.wait_until_ready()
    channel = bot.get_channel(GENERAL_CHAT)
    await channel.send('Conto!')

# ------------------------------ BP CIAO o SILENZIO -----------------------
@bot.command(aliases=['silenzio', 'ciao'])
async def saluto(ctx):
    channel = ctx.channel
    picture = discord.File('scout_sign.jpg')
    await channel.send(file=picture)


# ------------------------------ CITAZIONI BP -----------------------------
bp_quotes_file = open('bp_quotes.txt', 'r')
quotes = bp_quotes_file.readlines()
quotes = ['"' + quote[:-1] + '"' for quote in quotes]
bp_quotes_file.close()

@bot.command(aliases=['cit', 'quote', 'frase', 'cit.'])
async def citazione(ctx):
    channel = ctx.channel
    epiteto = random.choice(['mio caro', 'mia cara'])
    intro = f'Eccoti una mia bellissima citazione, {epiteto}!\n'
    quote = random.choice(quotes)
    await channel.send(intro + quote)

# --------------------------- RIMPROVERO PAROLACCE --------------------------
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

# count.start()
bot.run(TOKEN)

