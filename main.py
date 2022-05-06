import os
import io
import discord
from discord.ext import commands
import json
import requests
import PIL
from PIL import Image
from dotenv import load_dotenv

# discord bot
bot = commands.Bot(command_prefix="!")

# Opening JSON file with pfps. Add your open file and update it to match the name here
data = open('attributes.json')

# Folder locations for clean pfps, completed pfps, and outfits

save_img_folder = 'dressed_pfps/'
pfp_folder = 'clean_pfps/'
outfits_folder = 'outfits/'

# Returns JSON object as a dictionary
pfp_atts = json.load(data)


# list of the various outfits you want to offer. these should match the filename on the outfit pngs

outfits = ["suit", "blue", "vote", "pink","black", "cinco"]

# Search for the pfp id in the JSON dictionary and return the image URL associated with that id. You'll need to update the keys to match what's in your JSON delattr

# Need to add error handling


def get_pfp_img_url(id):
    for pfp in pfp_atts:
        if id == pfp['#']:
            return pfp['Image']


# Downloads the pfp from the image URL and saves it in a directory

def download_image(url, image_file_path):
    r = requests.get(url, timeout=4.0)
    if r.status_code != requests.codes.ok:
        assert False, 'Status code error: {}.'.format(r.status_code)

    with Image.open(io.BytesIO(r.content)) as im:
        im.save(image_file_path)

# Combines the pfp image with a transparent png of the attribute  and saves it to an output directory


def get_dressed(fit, pfp_id):
    url = (get_pfp_img_url(pfp_id))
    download_image(url, pfp_folder + str(pfp_id) + '.png')

# This combines the images

    pfp = Image.open(pfp_folder + str(pfp_id) + '.png')
    outfit = Image.open(outfits_folder + fit + '.png')

    pfp.paste(outfit, (0, 0), mask=outfit)
    pfp.save(save_img_folder + 'dressed' + str(pfp_id) + '.png')

    return


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !newfit command executes the get_dressed function and returns the resulting image. It accepts a value between 1 and 5000. Update this to use the command name you want and the values to fit the range of your project


@bot.command(name="newbrero", brief='Dress your pfp', description='This command will let you apply new fits to your pfp')
async def newfit(ctx, fit: str, pfp_id: int):
    try:
        if fit.lower() in outfits:
            if 0 <= pfp_id <= 5000:
                get_dressed(fit, str(pfp_id))
                await ctx.channel.send(file=discord.File(save_img_folder + 'dressed' + str(pfp_id) + '.png'))
        else:
            await ctx.send('Please enter a valid fit. Check !fits for options')
    except:
        await ctx.send('Please enter a valid number between 1 and 5000.')

# Lists the different "fits" available. This just returns the outfits list on new lines


@bot.command(brief='List avaiable fits', description='This command will list the different outfits available to you')
async def fits(ctx):
    await ctx.send('**List of Fits (please choose from one of the below)**\n\n' + "\n".join(outfits))

# Lets user know when they enter an invalid command


@bot.event
async def on_command_error(ctx, error):
    # or discord.ext.commands.errors.CommandNotFound as you wrote
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command, please check !help for a list of available commands")

load_dotenv()

bot.run(os.getenv('TOKEN'))
