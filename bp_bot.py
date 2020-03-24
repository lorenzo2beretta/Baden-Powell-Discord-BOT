import random
import discord
import os
from sys import argv
from datetime import datetime
from discord.ext import commands, tasks

with open('token', 'r') as file:
    TOKEN = file.read()
DEBUG_CHAT = 691024389730336842
REPARTO_CHAT = 690344893675339962
GENERAL_CHAT = DEBUG_CHAT if len(argv[1]) else REPARTO_CHAT

bot = commands.Bot(command_prefix=['bp ', 'BP ', 'B.P. ', 'b.p. '])
bot.description = 'Sono il fondatore del moviemento Scout!'

@bot.event
async def on_ready():
    print('Bot is Ready.')

# ------------------- FUNZIONI DA CHIAMARE PERIODICAMENTE --------------------
# Decorator that takes a datetime objects or list of datetime objects as input
def scheduled_loop(timestamps):
    if not isinstance(timestamps, list):
        timestamps = [timestamps]
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await bot.wait_until_ready()
            is_time = lambda dt: (datetime.now() - dt).seconds < 60
            if any([is_time(dt) for dt in timestamps]):
                await func(*args, **kwargs)
        return tasks.loop(seconds=60)(wrapper)
    return decorator

# --------------------------- PERIODICHE CITAZIONI DI BP ----------------------
with open('bp_quotes.txt', 'r') as file:
    bp_quotes = file.readlines()
    bp_quotes = ['"' + quote[:-1] + '"' for quote in bp_quotes]

@scheduled_loop(datetime.strptime('18:00', '%H:%M'))
async def citazione():
    channel = bot.get_channel(GENERAL_CHAT)
    post = 'Eccovi una mia bellissima citazione!\n'
    post += random.choice(bp_quotes)
    await channel.send(post)

# ------------------------- PERIOCDICHE COPPIE ---------------------------
@scheduled_loop(datetime.strptime('14:00', '%H:%M'))
async def coppia():
    channel = bot.get_channel(GENERAL_CHAT)
    users = channel.guild.members
    user1, user2 = random.sample(users, 2)
    adjectives = ['bellissima', 'pazzesca', 'promettente', 'fichissima']
    post = 'La '
    post += random.choice(adjectives)
    post += ' coppia del giorno è costituita da '
    post += user1.mention + ' e '
    post += user2.mention + '.'
    await channel.send(post)

# ------------------------- PROIEZIONE FOTO -------------------------------
picture_times = ['13:00', '15:00', '17:00', '19:00']
picture_times = [datetime.strptime(s, '%H:%M') for s in picture_times]
picture_names = os.listdir('./foto_campi/')

@scheduled_loop(picture_times)
async def proiezione_foto(ctx):
    channel = bot.get_channel(GENERAL_CHAT)
    picture = './foto_campi/' + random.choice(picture_names)
    post = 'Ecco una foto di me da giovane!'
    await channel.send(post, file=discord.File(picture))

# ------------------------ AVVISIO POSTA -----------------------------------
@scheduled_loop(datetime.strptime('21:30', '%H:%M'))
async def avviso_posta():
    channel = bot.get_channel(GENERAL_CHAT)
    post = '**POSTA ANONIMA**\n\n'
    with open('posta_anonima', 'r') as file:
        post += file.read()
    await channel.send(post)

# ------------------------------ BP SILENZIO -------------------------------
scout_sign_picture = discord.File('scout_sign.jpg')

@bot.command(aliases=['saluto', 'zitti'])
async def silenzio(ctx):
    channel = ctx.channel    
    await channel.send(file=scout_sign_picture)

# --------------------------- RIMPROVERO PAROLACCE --------------------------
with open('bad_words.txt', 'r') as file:
    bad_words = file.read()
    bad_words = sorted(bad_words.split(), key=lambda s: len(s), reverse=True)
    
async def reproach(message):
    channel = message.channel
    content = message.content
    epiteto = random.choice(['bello', 'bella'])
    word_list = ''.join(content.split())
    word_list = word_list.lower()
    for word in bad_words:
        if word in word_list:
            stars = '**' + '\*' * (len(word) - 2) + '**'
            censored = word[:1] + stars + word[-1:]
            post = 'Non si dice {}, {}!'.format(censored, epiteto)
            await channel.send(post)
            return True
    return False

# -------------------------- RIMPROVERO GIF --------------------------------
class gif_handler():
    gif_msg = []
    
    def __init__(self, max_gif=5, max_time=120):
        self.max_gif = max_gif
        self.max_time = max_time
    
    async def add(self, message):
        if len(message.embeds) == 0:
            return
        dt = datetime.utcnow()
        is_recent = lambda msg: (dt - msg.created_at).seconds < self.max_time
        self.gif_msg = [msg for msg in self.gif_msg if is_recent(msg)]
        self.gif_msg += [message]
        if len(self.gif_msg) > self.max_gif:
            channel = message.channel
            await channel.send(file=discord.File('stop_sign.jpg'))
            post = 'Ragazzi, mi avete ricorperto di GIF!'
            await channel.send(post)

gif_cop = gif_handler()            

# ------------------------- SERVIZIO DI POSTA ANONIMA ----------------------
async def anonymous_mail(message):
    channel = message.channel
    content = message.content
    chat_channel = bot.get_channel(GENERAL_CHAT)
    private_post = 'Scriverò quanto mi hai detto in forma anonima sulla chat.'
    await channel.send(private_post)
    public_post = '**Messaggio Anonimo:** ' + content
    await chat_channel.send(public_post)

# ----------------- GESTORE DELLE AZIONI INNESCATE DA UN MESSAGGIO ----------
@bot.event
async def on_message(message):
    # waits commands to be processed
    await bot.process_commands(message)    
    if message.author.bot:
        return
    
    await gif_cop.add(message)    
    reproached = await reproach(message)
    channel = message.channel
    if isinstance(channel, discord.channel.DMChannel) and not reproached:
        await anonymous_mail(message)        

proiezione_foto.start()
avviso_posta.start()
coppia.start()
citazione.start()    
bot.run(TOKEN)