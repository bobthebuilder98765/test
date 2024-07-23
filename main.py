import discord
from discord.ui import Button, View
from discord.ext import commands
import os
import asyncio
from webserver import keep_alive

token = os.environ.get('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

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

@bot.command()
async def spawn(ctx):
    view = GameButtonView()
    await ctx.send("Click a button to find players for a game.", view=view)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.data['component_type'] == 2:  # 2 corresponds to a button
        game = interaction.data['custom_id']
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

@bot.command()
async def add(ctx, name: str, role: str, emoji: str):
    games[name] = {"style": discord.ButtonStyle.blurple, "role": role, "emoji": emoji}
    await ctx.send(f"Added new game: {name} with role: {role} and emoji: {emoji}")

keep_alive()
bot.run(token)
