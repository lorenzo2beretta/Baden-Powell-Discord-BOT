from discord.ext import commands

TOKEN = 'NjkxMDIyNjg0NDk0MTAyNTM5.Xnc4CQ.cu5Mvj7uYPj0NmwnPX9jwV9QSHQ'
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
        
'''
@client.event
async def on_message(message):
    author = message.author
    if author.bot:
        return
    content = message.content
    channel = message.channel
    answer = '{.name} is wrong, "{}" is false.'.format(author, content)
    await channel.send(answer)
'''

client.run(TOKEN)

