import os
from discord.ext import commands
import discord
from dotenv import load_dotenv

from alpaca import api
from yahoo import get_top_trending_stocks, get_stock_info
from telescope import get_options_data
from ms_finance import get_stock_news

load_dotenv()

# Set up the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)



@bot.command()
async def commands(ctx):
    embed = discord.Embed(
        title="Alchemy Bot Commands",
        color=discord.Color.blue(),
        description="Here are the available commands for the Alchemy Bot:"
    )

    commands = {
        '!top_trending': 'Shows the top 5 trending stocks.',
        '!stock_info <symbol>': 'Fetches and displays information about the stock with the given symbol.',
        '!options <symbol>': 'Fetches and displays options data for the stock with the given symbol.',
        '!stock_news <performance_id>': 'Fetches and displays news for the stock with the given performance id.',
        '!hello': 'A test command to ensure that the bot is working.'
    }

    for command, description in commands.items():
        embed.add_field(name=command, value=description, inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def top_trending(ctx):
    stocks = get_top_trending_stocks()
    
    # Create an embed object
    embed = discord.Embed(
        title="Top 5 Trending Stocks",
        color=discord.Color.blue()
    )
    
    # Add fields to the embed for each stock symbol
    for index, symbol in enumerate(stocks):
        embed.add_field(name=f"Stock {index + 1}", value=symbol, inline=False)
    
    # Send the embed message
    await ctx.send(embed=embed)

@bot.command()
async def stock_info(ctx, symbol):
    try:
        stock = get_stock_info(symbol)
        if stock is None:
            await ctx.send(f"Could not find stock information for {symbol}.")
            return

        # Format and display the stock information as an embed
        embed = discord.Embed(
            title=f"{symbol} Stock Info",
            color=discord.Color.blue()
        )
        embed.add_field(name="Price", value=stock["price"], inline=False)
        embed.add_field(name="Market Cap", value=stock["market_cap"], inline=False)
        embed.add_field(name="Volume", value=stock["volume"], inline=False)
        embed.add_field(name="Day High", value=stock["day_high"], inline=False)
        embed.add_field(name="Day Low", value=stock["day_low"], inline=False)
        await ctx.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await ctx.send("An error occurred while fetching the stock information.")

@bot.command()
async def options(ctx, symbol):
    try:
        options_data = get_options_data(symbol)
        if options_data is None:
            await ctx.send(f"Could not find options data for {symbol}.")
            return

        embed = discord.Embed(
            title=f"{symbol} Options Data",
            color=discord.Color.blue()
        )
        
        for option in options_data[:10]:  # Display only the first 10 options for simplicity
            option_info = f"Contract: {option['contractSymbol']} | Strike: {option['strike']} | Last Price: {option['lastPrice']} | Volume: {option.get('volume', 'N/A')}"
            embed.add_field(name="Option", value=option_info, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await ctx.send("An error occurred while fetching the options data.")

@bot.command()
async def stock_news(ctx, performance_id):
    try:
        news_data = get_stock_news(performance_id)
        if news_data is None or len(news_data) == 0:
            await ctx.send(f"Could not fetch stock news for {performance_id}.")
            return

        embed = discord.Embed(
            title=f"Stock News for {performance_id}",
            color=discord.Color.blue()
        )

        # Display only the first 5 news items for simplicity
        for i, news in enumerate(news_data[:5]):
            news_title = news['title']
            news_published_date = news['publishedDate']
            news_source = news['sourceName']
            news_info = f"{news_title}\nSource: {news_source}\nPublished: {news_published_date}"
            embed.add_field(name="News", value=news_info, inline=False)

        await ctx.send(embed=embed)

    except Exception as e:
        print("Error:", e)
        await ctx.send("An error occurred while fetching the stock news.")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I'm your stock trading bot!")

# Run the bot
if __name__ == "__main__":
    discord_token = os.getenv('DISCORD_TOKEN')
    bot.run(discord_token)
