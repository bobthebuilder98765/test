import discord
from discord.ui import Button, View
from discord.ext import commands
import os
from webserver import keep_alive

# Fill in your token here
token = os.environ.get('token')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

games = {
    "minecraft": {"style": discord.ButtonStyle.blurple, "role": "Minecraft", "emoji": "⛏️"},
    "fortnite": {"style": discord.ButtonStyle.blurple, "role": "Fortnite", "emoji": "🌪️"},
    # Add other games here...
}

class GameButtonView(View):
    def __init__(self):
        super().__init__()
        for game, style in games.items():
            self.add_item(Button(style=games[game]['style'], label=game, custom_id=game, emoji=games[game]['emoji']))

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

                # Acknowledge the interaction
                await interaction.response.defer()

                # Send the message to the specific channel
                channel_id = 1156180116024590396  # Change this to your desired channel ID
                channel = bot.get_channel(channel_id)

                # Check if the message has already been sent
                messages = await channel.history().flatten()
                sent_messages = [msg for msg in messages if msg.embeds and msg.embeds[0].title == embed.title]

                if not sent_messages:
                    await channel.send(embed=embed)
            else:
                await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)
        else:
            # Acknowledge the interaction and send a hidden message to the user
            await interaction.response.send_message("You need to be in a voice channel to use this command.", ephemeral=True)

keep_alive()
bot.run(token)
