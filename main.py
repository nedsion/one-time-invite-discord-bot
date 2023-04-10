import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
import os
import random

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
        changepresence.start()
    except Exception as e:
        print(f"Error syncing commands: {e}")


@tasks.loop(seconds=30)
async def changepresence():
    global x
    total_members = []

    for guild in bot.guilds:
        total_members.append(guild.member_count)
    total_members_count = sum(total_members)
    game = iter(
        [
            f"nedsion.xyz | {len(bot.guilds)} servers!",
            f"nedsion.xyz | {total_members_count} members!",
            f"nedsion.xyz | Have a nice day!",
            f"nedsion.xyz | /help",
        ]
    )
    for x in range(random.randint(1, 4)):
        x = next(game)
    await bot.change_presence(activity=discord.Game(name=x))

@bot.tree.command(name="help", description="Get help")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Help",
        description="Here is a list of all my commands",
        color=discord.Color.green(),
    )
    embed.add_field(
        name="Commands",
        value="`/help` - Get help\n`/onetimeinvite` - Get an invite link for this server",
        inline=False,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="onetimeinvite", description="Get an invite link for this server")
@app_commands.describe(channel="Invite Channel", invite_max_age="Invite Max Age", invite_max_uses="Invite Max Uses", number_of_link="Number of Link")
async def one_time_invite(interaction: discord.Interaction, channel: discord.TextChannel, invite_max_age: int, invite_max_uses: int, number_of_link: int):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.guild_permissions.manage_guild:
        try:
            invites = []
            for i in range(number_of_link):
                invite = await channel.create_invite(max_age=invite_max_age, max_uses=invite_max_uses)
                invites.append(str(invite))
                link = "\n".join(invites)
            with open(f'invite-{interaction.user.id}.txt', 'w') as f:
                f.write(link)
                f.close()
            await interaction.followup.send(f"Here is your invite:", ephemeral=True, file=discord.File(f"invite-{interaction.user.id}.txt"))
            os.remove(f"invite-{interaction.user.id}.txt")

        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
    else:
        await interaction.followup.send("You do not have permission to use this command", ephemeral=True)


bot.run("BOT_TOKEN")
