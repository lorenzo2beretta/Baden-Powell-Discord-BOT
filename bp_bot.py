import random
import discord
import os
import sys
from datetime import datetime
from discord.ext import commands, tasks

# legge il token necessario per associare il codice al bot discord il token è 
# letto da un file locale listato in .gitignore per evitare che venga "corrotto".
with open('token', 'r') as file:
    TOKEN = file.read()

# id che si possono trovare nell'interfaccia di discord in "developer mode"
LORENZO_ID = 691214172360409117 
DEBUG_CHAT = 691024389730336842
REPARTO_CHAT = 690344893675339962
CAPANNONE_CHAT = 691315170823372811

# modalità debug per testare il bot prima di lanciarlo sul server ufficiale
if len(sys.argv) > 1:
    REPARTO_CHAT = DEBUG_CHAT
    CAPANNONE_CHAT = DEBUG_CHAT
else:
    # se non sono in modalità debugger scrivo in un file logger per avere un 
    # report di eventuali crush
    logger = open('logger', 'w')
    sys.stderr = logger
    sys.stdout = logger

# inizializzazione del bot e impostazione dei prefissi per chiamare un comando
command_prefix = ['bp ', 'BP ', 'B.P. ', 'b.p. ', 'Bp ', 'B.p. ']
bot = commands.Bot(command_prefix=command_prefix)
bot.description = 'Sono il fondatore del moviemento Scout!'

@bot.event
async def on_ready():
    print('Bot is Ready.')
    
# ---------------------- INVIO RICORDELLE LUPUS -----------------------------
#@bot.command()
#async def prova(ctx):
#    user = bot.get_user(LORENZO_ID)
#    channel = user.dm_channel
#    if channel is None:
#        await user.create_dm()
#        channel = user.dm_channel
#    post = 'Ciao Lore'
#    await channel.send(post)
#   
    
# --------------------------- COMDANDO DELLA BUONANOTTE --------------------
# questo comando invia una foto di stelle e una cit dei MCR
@bot.command(aliases=['notte', 'Notte', 'Buonanotte'])
async def buonanotte(ctx):
    channel = ctx.channel
    picture_stelle = os.listdir('./foto_stelle/')
    picture = './foto_stelle/' + random.choice(picture_stelle)
    post = 'Buonanotte ragazzi, che le stelle vi guidino sempre e '
    post += 'la strada vi porti lontano!'
    await channel.send(post, file=discord.File(picture))

# dato che gli aliases non possono contenere spazi ho creato questa funzione
# ausiliaria che accetta le stringhe "bp buona notte" come comandi
@bot.command(aliases=['Buona'])
async def buona(ctx, *args):
    if len(args) > 0 and args[0] == 'notte':
        await buonanotte(ctx)
    
# ------------------- FUNZIONI DA CHIAMARE PERIODICAMENTE --------------------
# definisco un decorator che prende un datetime timestamp o una lista di
# timestamps e trasforma una funzione in un task che viene eseguito ogni
# giorno in quegli orari
def scheduled_loop(timestamps):
    if not isinstance(timestamps, list):
        timestamps = [timestamps]
    def decorator(func):
        async def wrapper(*args, **kwargs):
            await bot.wait_until_ready()
            is_time = lambda dt: (datetime.now() - dt).seconds < 60
            if any(is_time(dt) for dt in timestamps):
                await func(*args, **kwargs)
        return tasks.loop(seconds=60)(wrapper)
    return decorator

# --------------------------- PERIODICHE CITAZIONI DI BP ----------------------
# invia su chat generale una periodica citazione di bp letta da file
with open('bp_quotes.txt', 'r') as file:
    bp_quotes = file.readlines()
    bp_quotes = ['"' + quote[:-1] + '"' for quote in bp_quotes]

@scheduled_loop(datetime.strptime('20:00', '%H:%M'))
async def periodica_citazione():
    channel = bot.get_channel(REPARTO_CHAT)
    post = 'Eccovi una mia bellissima citazione!\n'
    post += random.choice(bp_quotes)
    await channel.send(post)

# ------------------------ COMANDO CITAZIONI DI BP ----------------------------
# invia una citazione di bp a richiesta
@bot.command(aliases=['cit', 'quote', 'frase'])
async def citazione(ctx):
    channel = ctx.channel
    author = ctx.author
    post = 'Eccoti una mia bellissima citazione {}!\n'.format(author.mention)
    post += random.choice(bp_quotes)
    await channel.send(post)

# ------------------------- PROIEZIONE FOTO -------------------------------
# invia sulla chat generale foto di reparto random ad orari fissati 
picture_times = ['13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00']
picture_times = [datetime.strptime(s, '%H:%M') for s in picture_times]

@scheduled_loop(picture_times)
async def proiezione_foto():
    channel = bot.get_channel(REPARTO_CHAT)
    picture_campi = os.listdir('./foto_campi/')
    picture = './foto_campi/' + random.choice(picture_campi)
    post = 'Ecco una foto di me da giovane!'
    await channel.send(post, file=discord.File(picture))
    post = 'Se vuoi altre foto scrivi **bp foto**.'
    await channel.send(post)

# -------------------------- COMANDO FOTO ---------------------------------
# invia una foto di reparto random a comando
@bot.command(aliases=['pic', 'immagine'])
async def foto(ctx):
    channel = ctx.channel
    picture_campi = os.listdir('./foto_campi/')
    picture = './foto_campi/' + random.choice(picture_campi)
    author = ctx.author
    post = 'Ecco la tua foto {}.'.format(author.mention)
    await channel.send(post, file=discord.File(picture))
    
# ------------------------ AVVISIO POSTA -----------------------------------
# ricorda al reparto come funziona il servizio di posta anonima
@scheduled_loop(datetime.strptime('15:30', '%H:%M'))
async def avviso_posta():
    channel = bot.get_channel(CAPANNONE_CHAT)
    post = '**POSTA ANONIMA**\n\n'
    with open('posta_anonima', 'r') as file:
        post += file.read()
    await channel.send(post)

# ------------------------------ BP SILENZIO -------------------------------
# comando che invia l'immagine del saluto scout, per ottenere il silenzio
@bot.command(aliases=['saluto', 'zitti'])
async def silenzio(ctx):
    channel = ctx.channel    
    await channel.send(file=discord.File('scout_sign.jpg'))
    
# --------------------------- RIMPROVERO PAROLACCE --------------------------
# ogni qualvolta un messaggio viene inviato su una chat che il bot può leggere
# controlla se sono presenti parolacce (tratte da un file) in caso affermativo
# rimprovera chi ha inviato queste parolacce
with open('bad_words.txt', 'r') as file:
    bad_words = file.read()
    bad_words = sorted(bad_words.split(), key=lambda s: len(s), reverse=True)
    
async def reproach(message):
    channel = message.channel
    content = message.content
    epiteto = random.choice(['bello', 'bella'])
    
    # provo tutte le combinazioni di 1, 2 o 3 parole adiacenti
    words = content.lower().split()
    two_words = [x + y for x, y in zip(words, words[1:])]
    three_words = [x + y + z for x, y, z in zip(words, words[1:], words[2:])]
    words += two_words
    words += three_words
    
    for word in words:
        # controllo se word è una parola volgare
        if word in bad_words:
            # NOTA: "**text**" stampa "text" in grassetto e "\*" stampa "*"
            stars = '**' + '\*' * (len(word) - 2) + '**'
            censored = word[:1] + stars + word[-1:]
            post = 'Non si dice {}, {}!'.format(censored, epiteto)
            await channel.send(post)
            return True
    return False

# -------------------------- RIMPROVERO GIF --------------------------------
# controlla se negli ultimi max_time secondi sonon state mandate più di max_gif 
# gif da un account umano e in caso affermativo rimprovera
class gif_handler():
    gif_msg = []
    
    def __init__(self, max_gif=5, max_time=120):
        self.max_gif = max_gif
        self.max_time = max_time
    
    # aggiunge un  messaggio alla coda dei messaggi avvenuti negli ultimi
    # max_time seconodi
    async def add(self, message):
        # controlla se il messaggion contiene una gif
        if len(message.embeds) == 0:
            return
        dt = datetime.utcnow()
        # funzione che decide se un messagio è recente
        is_recent = lambda msg: (dt - msg.created_at).seconds < self.max_time
        # conservo solo i messaggi recenti
        self.gif_msg = [msg for msg in self.gif_msg if is_recent(msg)]
        # aggiungo l'ulitmo messaggio
        self.gif_msg += [message]
        if len(self.gif_msg) > self.max_gif:
            channel = message.channel
            await channel.send(file=discord.File('stop_sign.jpg'))
            post = 'Ragazzi, mi avete ricorperto di GIF!'
            await channel.send(post)

# istanzio la classe gif_handler nell'oggetto gif_cop (poliziotto delle gif XD)
gif_cop = gif_handler()            

# -------------------------- COMANDO PRIMA PERSONA --------------------------
# questo comando permette all'account di Lorenzo di far parlare 
# il bot in prima persona
@bot.command()
async def parla(ctx, *args):
    author = ctx.author
    channel = ctx.channel
    
    if author.id != LORENZO_ID or len(args) == 0:
        post = 'Non vorrai mettermi in bocca parole non mie!?'
        await channel.send(post)
        return
    # il primo argomento determina quale chat usare per la comunicazione
    if args[0] == 'capannone':
        chat_channel = bot.get_channel(CAPANNONE_CHAT)
    else:
        chat_channel = bot.get_channel(REPARTO_CHAT)
    await chat_channel.send(' '.join(args[1:]))

# ------------------------- SERVIZIO DI POSTA ANONIMA ----------------------
# quando il bot riceve un messaggio privato, lo riposta sulla chat del lupus
async def anonymous_mail(message):
    channel = message.channel
    content = message.content
    chat_channel = bot.get_channel(CAPANNONE_CHAT)
    
    private_post = 'Scriverò quanto mi hai detto in forma anonima sulla chat.'
    await channel.send(private_post)
    public_post = '**Messaggio Anonimo:** ' + content
    await chat_channel.send(public_post)

# ----------------- GESTORE DELLE AZIONI INNESCATE DA UN MESSAGGIO ----------
# questa funzione viene chiamata ogni volta che il bot legge un messaggio su
# una qualsiasi chat alla quale ha accesso (tutte visto che ha permessi da
# amministratore).
@bot.event
async def on_message(message):
    # attende che i messaggi comando vengano interpretati come tali
    await bot.process_commands(message)
    # se il messaggio è stato mandato da un bot non fa nulla
    if message.author.bot:
        return
    
    await gif_cop.add(message)
    reproached = await reproach(message)
    channel = message.channel
    is_private = isinstance(channel, discord.channel.DMChannel)
    content = message.content
    is_command = any(content.startswith(s) for s in command_prefix)
    # lancia il servizio di posta privata solo se il messaggio non è un comando
    # e non è volgare
    if is_private and not is_command and not reproached:
        await anonymous_mail(message)        

# lancio i task periodici e faccio partire il bot associandolo al token
proiezione_foto.start()
avviso_posta.start()
periodica_citazione.start()    
bot.run(TOKEN)
