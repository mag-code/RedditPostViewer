import discord
import praw
import os
import dotenv
from discord.ext import commands
from dotenv import *
# Get the path to the directory this file is in
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
password = os.getenv("password")
user_agent = os.getenv("user_agent")
username = os.getenv("username")
token = os.getenv("token")

reddit = praw.Reddit(
     client_id=client_id,
     client_secret=client_secret,
     password=password,
     user_agent=user_agent,
     username=username,
)

botDescription="Bot"
intents = discord.Intents.all()
client = commands.Bot(command_prefix="?", help_command=None, description=botDescription, intents=intents)

# Discord event handler for when the bot is ready
@client.event
async def on_ready():
    print('Bot is ready.')

# Discord event handler for when a message is sent
@client.event
async def on_message(message):
    # Only respond to messages that start with "!help"
    if message.content.startswith('!help'):
            await message.channel.send('The available commands are !hot, !new, !top, !help.  The format to use these commands are !command (subreddit)')
            return
    elif message.content.startswith('!new'):
        try:
            subreddit_name = message.content.split(' ')[1]
            subreddit = reddit.subreddit(subreddit_name)  
# Get the 5 newest posts from the subreddit
            newest_posts = subreddit.new(limit=5)
# Build a response message with the post titles and URLs
            response = 'Newest posts from r/{}:\n'.format(subreddit.display_name)
            for post in newest_posts:
                response += '- {} ({})\n'.format(post.title, post.url)
            # Send the response message
            await message.channel.send(response)
        except IndexError:
            await message.channel.send('Please provide a subreddit name after the command. For example, !new (subreddit_name)')
        except Exception as e:
            await message.channel.send('Error fetching the subreddit. Please check if the subreddit exists.')
            print(f'Error: {e}')
# Only respond to messages that start with "!hot"
    elif message.content.startswith('!hot'):
        try:
            subreddit_name = message.content.split(' ')[1]
            subreddit = reddit.subreddit(subreddit_name)
# Get the 5 hottest posts from the subreddit
            hottest = subreddit.hot(limit=5)
# Build a response message with the post titles and URLs
            response = 'Hottest posts from r/{}:\n'.format(subreddit.display_name)
            for post in hottest:
                response += '- {} ({})\n'.format(post.title, post.url)
            # Send the response message
            await message.channel.send(response)
        except IndexError:
            await message.channel.send('Please provide a subreddit name after the command. For exmaple, !hot (subreddit_name)')
        except Exception as e:
            await message.channel.send('Error fetching the subreddit. Please check if the subreddit exists.')
            print(f'Error: {e}')
# Only respond to messages that start with "!top"
    elif message.content.startswith('!top'):
        try:
            subreddit_name = message.content.split(' ')[1]
            subreddit = reddit.subreddit(subreddit_name)
        # Get the 5 top posts from the subreddit
            top = subreddit.top(limit=5)
# Build a response message with the post titles and URLs
            response = 'Top posts from r/{}:\n'.format(subreddit.display_name)
            for post in top:
                response += '- {} ({})\n'.format(post.title, post.url)
# Send the response message
            await message.channel.send(response)
        except IndexError:
            await message.channel.send('Please provide a subreddit name after the command. For exmaple, !top (subreddit_name)')
        except Exception as e:
            await message.channel.send('Error fetching the subreddit. Please check if the subreddit exists.')
            print(f'Error: {e}')

# Start the bot
client.run(token)
