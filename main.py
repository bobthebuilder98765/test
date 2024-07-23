import discord
from discord import app_commands
from discord.ui import Button, View
from discord.ext import commands
import os
import asyncio
from webserver import keep_alive

token = os.environ.get('token')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)

games = {
    "minecraft": {"style": discord.ButtonStyle.blurple, "role": "Minecraft", "emoji": "⛏️"},
    "fortnite": {"style": discord.ButtonStyle.blurple, "role": "Fortnite", "emoji": "🌪️"},
    "scribble": {"style": discord.ButtonStyle.blurple, "role": "Scribble", "emoji": "🖍️"},
    "gartic phone": {"style": discord.ButtonStyle.blurple, "role": "Gartic Phone", "emoji": "📱"},
    "valorant": {"style": discord.ButtonStyle.blurple, "role": "Valorant", "emoji": "🔫"},
    "cs": {"style": discord.ButtonStyle.blurple, "role": "CS:GO", "emoji": "💣"},
    "Lethal Company": {"style": discord.ButtonStyle.blurple, "role": "Lethal Company", "emoji": "👹"},
    "VR GAMES": {"style": discord.ButtonStyle.blurple, "role": "VR GAMES", "emoji": "👓"},
    "Brawlhalla": {"style": discord.ButtonStyle.blurple, "role": "Brawlhalla", "emoji": "⚔️"},
    "ARMA III": {"style": discord.ButtonStyle.blurple, "role": "ARMA III", "emoji": "🪖"},
    "DayZ": {"style": discord.ButtonStyle.blurple, "role": "DayZ", "emoji": "🧟"},
    "Stick Fight: The Game": {"style": discord.ButtonStyle.blurple, "role": "Stick Fight: The Game", "emoji": "👨‍🦯"},
    "The Finals": {"style": discord.ButtonStyle.blurple, "role": "The Finals", "emoji": "🧱"},
    "Tank Team": {"style": discord.ButtonStyle.blurple, "role": "Tank Team", "emoji": "🚛"}
}

class GameButtonView(View):
    def __init__(self):
        super().__init__()
        for game, style in games.items():
            self.add_item(Button(style=style['style'], label=game, custom_id=game, emoji=style['emoji']))

@bot.tree.command(name="spawn", description="Spawn game buttons")
async def spawn(interaction: discord.Interaction):
    view = GameButtonView()
    await interaction.response.send_message("Click a button to find players for a game.", view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        custom_id = interaction.data.get('custom_id')
        if custom_id in games:
            game = custom_id
            if interaction.user.voice:
                voice_channel = interaction.user.voice.channel
                role_name = games[game]['role']
                role = discord.utils.get(interaction.guild.roles, name=role_name)
                if role:
                    users_with_role = [member.mention for member in role.members if member != interaction.user]
                    users_with_role_str = ' '.join(users_with_role)
                    embed = discord.Embed(
                        title=f"{interaction.user.name} is looking to play {game}",
                        description=f"{users_with_role_str}\n\n{interaction.user.mention} is waiting at voice: {voice_channel.mention}"
                    )
                    channel = bot.get_channel(1156180116024590396)
                    await interaction.response.defer()
                    await channel.send(embed=embed)
                else:
                    await interaction.response.defer()
                    channel = bot.get_channel(1156180116024590396)
                    message = await channel.send("You need to be in a voice channel to use this command. " + interaction.user.mention)
                    await asyncio.sleep(10)
                    await message.delete()
            else:
                await interaction.response.defer()
                channel = bot.get_channel(1155946685676146709)
                message = await channel.send("You need to be in a voice channel to use this command. " + interaction.user.mention)
                await asyncio.sleep(10)
                await message.delete()

@bot.tree.command(name="addbutton", description="Add a new game button")
@app_commands.describe(
    name="The name of the game",
    role="The role associated with the game",
    emoji="The emoji for the game button"
)
async def addbutton(interaction: discord.Interaction, name: str, role: str, emoji: str):
    games[name] = {"style": discord.ButtonStyle.blurple, "role": role, "emoji": emoji}
    await interaction.response.send_message(f"Added new game button: {name} with role: {role} and emoji: {emoji}")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.tree.sync()

keep_alive()
bot.run(token)
