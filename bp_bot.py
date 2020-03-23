import random
import discord
from sys import argv
from datetime import datetime
from discord.ext import commands, tasks

with open('token', 'r') as file:
    TOKEN = file.read()
# Se un argomento viene fornito al bot allora mi trovo in modalità debug
# e il bot scrive sulla chat del server "bot arena"
DEBUG_CHAT = 691024389730336842
REPARTO_CHAT = 690344893675339962
GENERAL_CHAT = DEBUG_CHAT if len(argv) > 1 else REPARTO_CHAT

bot = commands.Bot(command_prefix=['bp ', 'BP ', 'B.P. ', 'b.p. '])
bot.description = 'Sono il fondatore del moviemento Scout!'

@bot.event
async def on_ready():
    print('Bot is Ready.')

# ------------------- FUNZIONI DA CHIAMARE PERIODICAMENTE --------------------
@tasks.loop(seconds=60, count=3)
async def coppia():
    start_time = datetime.strptime('14:00', '%H:%M')
    diff = datetime.now() - start_time
    if diff.seconds < 60:
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

# ------------------------------ BP SILENZIO -------------------------------
scout_sign_picture = discord.File('scout_sign.jpg')

@bot.command(aliases=['silenzio', 'zitti'])
async def saluto(ctx):
    channel = ctx.channel    
    await channel.send(file=scout_sign_picture)


# ------------------------------ CITAZIONI BP -----------------------------
with open('bp_quotes.txt', 'r') as file:
    quotes = file.readlines()
    quotes = ['"' + quote[:-1] + '"' for quote in quotes]

@bot.command(aliases=['cit', 'quote', 'frase', 'cit.'])
async def citazione(ctx):
    channel = ctx.channel
    epiteto = random.choice(['mio caro', 'mia cara'])
    post = f'Eccoti una mia bellissima citazione {}!\n'.format(epiteto)
    post += random.choice(quotes)
    await channel.send(post)

# --------------------------- RIMPROVERO PAROLACCE --------------------------
with open('bad_words.txt', 'r') as file:
    content = file.read()
    bad_words = sorted(content.split(), key=lambda s: len(s), reverse=True)
    
async def reproach(channel, content):
    epiteto = random.choice(['bello', 'bella'])
    word_list = ''.join(content.split())
    for word in bad_words:
        if word in word_list:
            stars = '**' + '\*' * (len(word) - 2) + '**'
            censored = word[:1] + stars + word[-1:]
            post = 'Non si dice {}, {}!'.format(censored, epiteto)
            await channel.send(post)
            return True
    return False

# Struttura dati che conserva i messaggi con url degli ultimi 2 minuti

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

gif_cop = gif_handler(max_gif=1)            

@bot.event
async def on_message(message):
    # waits commands to be processed
    await bot.process_commands(message)    
    author = message.author
    channel = message.channel
    content = message.content
    if author.bot:
        return
    
    await gif_cop.add(message)
        
    reproached = await reproach(channel, content)
    # Spotted bot part
    if isinstance(channel, discord.channel.DMChannel) and not reproached:
        chat_channel = bot.get_channel(GENERAL_CHAT)
        private_post = 'Scriverò quanto mi hai detto in forma anonima sulla chat.'
        await channel.send(private_post)
        public_post = '**Messaggio Anonimo:** ' + content
        await chat_channel.send(public_post)
    
        
    

coppia.start()    
bot.run(TOKEN)