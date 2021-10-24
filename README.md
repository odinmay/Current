#  ⚡Current⚡ - a discord.py bot

![](https://i.imgur.com/vTv33yo.png)

### Features
- Manage Members and Roles
- Cards Against Discord! chat game(cards against humanity with user input answers)
- User Economy, simple integration to any Cog/Command
- Easily extendable with an included Base Cog you can use as a template
- Jokes, Movies, Magic the Gathering, 8 Ball ect.
- Well documented / beginner-friendly.
- Server chat history backup command



![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg)




# Administrator Cog Commands
- **.ping**: Prints the bots ping in ms
- **.kick**: Kicks target member
- **.ban**: Bans target member
- **.unban**: Unbans target member
- **.list_channels**: Pulls all of the guild channels and displays them in an Embed message
- **.emojis**: Print the total emojis available to the Guild
- **.server_birthday**: Prints the date the Guild was created at
- **.members**: Prints all of the members on the server
- **.boosters**: Print the server boosters of the guild and date they started boosting
- **.member_count**: Prints the # of members

# Entertainment Cog Commands
- **.8ball**: Ask it a question!
- **.flip**: Whats the most you ever lost in a coin toss?
- **.joke**: Tells a joke
- **.chuck**: Tells a Chuck Noris FACT
- **.magicians**: Displays random Magicians gif
- **.mtg**: Magic The Gathering card data from magicthegathering.io/scryfall
- **.mtg_art**: Magic The Gathering card art from magicthegathering.io/scryfall
- **.movie**: Displays a movies plot/rating/trailer
- **.sindarin**: Translates message into Elvish(Sindarin)
- **.spotify**: Shares what you are listening to on Spotify
- **.deflect**: Displays a random deflect gif

# Voicebot Cog Commands
- **.stream**: Streams a url / search from YouTube Soundcloud etc.
- **.volume**: Sets the bot volume percentage
- **.join**: Have the bot join your voice channel
- **.stop**: Cancels audio and disconnects bot from voice

# Bank Cog Commands
- **.balance**: Prints the balance in the users account
- **.add**: Adds money to users account
- **.sub**: Removes money from users account

# Games Cog Commands
- **.guess**: Guess a number 1-100, win money! (Internal Economy)
- **.beg**: Beg for a small amount of cash to be deposited to your account
- **.bet**: Simple game: 1% chance for 8x, 30% chance for 2x payout
- **.steal**: Attempt to steal $150 from a members account

# Cards Against Discord Cog Commands
- **.game_join**: Prints the bots ping in ms
- **.game_start**: Prints the bots ping in ms
- **.vote**: Prints the bots ping in ms



----
# Adding your own Cogs
More info - 
https://discordpy.readthedocs.io/en/stable/ext/commands/cogs.html

If you would like to extend the bot and add more functionality you can easily add your own Cog.
I have included a base_cog.py file you can use to get started. The process for adding a cog is very straghtforward and 
made especially easy with this base file.

1. Create a new .py file in the [cogs] directory. You may choose a relevant name.

    `cd cogs && touch new_cog.py`


2. Copy the contents of **base_cog.py** to your file
  
    `cp base_cog.py new_cog.py`


3. Rename **Base_New_Cog** to the name you want your cog class to have. There will be 2 references to update

  ```python 
from discord.ext import commands
import discord


        | rename |
        v        v
class Base_New_Cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

                  
def setup(bot):   | rename |
                    v        v
     bot.add_cog(Base_New_Cog(bot))

  ```
4. Add your Cog to ``main.py`` **extensions** list near top of file. Don't forget the comma!


5. Congrats! You have created your own Cog. Add commands and functionality and have fun!

# ToDo
- [ ] Refine Broad Exceptions
- [ ] Add Music player Queue Functionality
- [ ] Add more games to the bot
- [ ] Implement Tests
- [ ] Add more Admin functions(channel management, role management)
- [ ] Implement Rate Limits on some commands
- [ ] Improve the code with the help of the community!


If anyone is interested in helping feel free to submit a PR or reach out to me on discord @ Uhhhhknown#1823.
I am looking to learn and grow as well as help out when I can. Thanks!
