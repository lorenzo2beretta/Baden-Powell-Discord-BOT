from discord.ext import commands

TOKEN = 'NjkxMDIyNjg0NDk0MTAyNTM5.Xnc-5w.tuWvmSjZZ4O4DvJDHLJ8lF_OjJA'
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


client.run(TOKEN)

