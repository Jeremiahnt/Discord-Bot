import discord
from discord.ext import commands
from discord import *
import os
from pytube import YouTube

def scrape(url):
    yt = YouTube(
        url,
        use_oauth= True,
        allow_oauth_cache= True
    )
    
    title = (yt.title)
    title = f"{title.replace('/', '_').replace('|', '_').replace(' ', '_').replace(':','_')}" 
    filename=f'{title}.mp3'
    output_path= 'INSERT_TEMPORARY_DOWNLOAD_PATH'
    
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    audio_stream.download(output_path, filename)
    
    full_path = os.path.join(output_path, filename)
    return full_path
    
    
TOKEN = 'INSERT_TOKEN_HERE'
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    
    # Sync slash commands with Discord
    await bot.tree.sync() 
    print(f'Logged in as {bot.user.name}')

@bot.tree.command(name="pirate", description="Downloads the audio from YouTube URL")
async def pirate(interaction: discord.Interaction, url: str):
    await interaction.response.defer()
    filename = scrape(url) 
    if filename:
            try:
                # After downloading, the bot CURRENTLY does not have a proper file name... need to get it saved out of the scrape def()
                await interaction.followup.send(file=discord.File(f'{filename}'))
                os.remove(filename)
            except Exception as e:
                await interaction.followup.send(f"An error occurred: {str(e)}", ephemeral=True)
    else:
        await interaction.followup.send(f"Download failed, or failed to send file in time.")

@bot.tree.command(name="hello", description='Test command that texts "hello"')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}, this is the second slash command", ephemeral=True)

# @bot.tree.command(name="picture", description="Sends a specified file from hosted system.")
# async def hello(interaction: discord.Interaction):
#     await interaction.response.defer()

bot.run(TOKEN)