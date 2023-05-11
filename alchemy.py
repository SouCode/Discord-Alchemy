import os
import discord
from discord import Embed
from discord.ext import commands
import alpaca_trade_api as tradeapi
import traceback
import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import json
import os
from dotenv import load_dotenv

load_dotenv()


# Set up the Discord bot
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


# Set up the Alpaca API instance
api_key = os.environ['ALPACA_API_KEY']
secret_key = os.environ['ALPACA_SECRET_KEY']
base_url = os.environ['ALPACA_BASE_URL']
api = tradeapi.REST(api_key, secret_key, base_url, api_version='v2')


# YahooFinance ~ Trending Stocks 
def get_top_trending_stocks():
    rapidapi_key = os.environ['RAPIDAPI_KEY']
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-trending-tickers"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        top_stocks = data['finance']['result'][0]['quotes'][:5]
        return [stock['symbol'] for stock in top_stocks]
    else:
        print(f"Error fetching trending stocks: {response.status_code}")
        return []


@bot.command()
async def top_trending(ctx):
    stocks = get_top_trending_stocks()
    
    # Create an embed object
    embed = Embed(
        title="Top 5 Trending Stocks",
        color=discord.Color.blue()
    )
    
    # Add fields to the embed for each stock symbol
    for index, symbol in enumerate(stocks):
        embed.add_field(name=f"Stock {index + 1}", value=symbol, inline=False)
    
    # Send the embed message
    await ctx.send(embed=embed)



# YahooFinance ~  Stocks Quotes 
def get_stock_info(symbol):
    rapidapi_key = os.environ['RAPIDAPI_KEY']
    url = f"https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary?symbol={symbol}&region=US"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        return {
            "price": data["price"]["regularMarketPrice"]["raw"],
            "market_cap": data["summaryDetail"]["marketCap"]["raw"],
            "volume": data["summaryDetail"]["volume"]["raw"],
            "day_high": data["summaryDetail"]["dayHigh"]["raw"],
            "day_low": data["summaryDetail"]["dayLow"]["raw"],
        }
    else:
        print(f"Error fetching stock information: {response.status_code}")
        return None


# Yahoo Finance ~ Bot commands for Quotes and Options Data
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


# Telescope API ~  Options Data
def get_options_data(symbol):
    rapidapi_key = os.environ['RAPIDAPI_KEY']
    url = f"https://telescope-stocks-options-price-charts.p.rapidapi.com/options/{symbol}"
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "telescope-stocks-options-price-charts.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.text)
        options_data = data["optionChain"]["result"][0]["options"][0]["calls"]
        return options_data
    else:
        print(f"Error fetching options data: {response.status_code}")
        return None



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


# MS Finance API ~ Stock News
def get_stock_news(performance_id):
    rapidapi_key = os.environ['RAPIDAPI_KEY']
    url = "https://ms-finance.p.rapidapi.com/news/list"
    querystring = {"performanceId": performance_id}
    headers = {
        "X-RapidAPI-Key": rapidapi_key,
        "X-RapidAPI-Host": "ms-finance.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        print(f"Error fetching stock news: {response.status_code}")
        return None


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




# Add a simple command to test your bot
@bot.command()
async def hello(ctx):
    await ctx.send("Hello, I'm your stock trading bot!")



# Run the bot
if __name__ == "__main__":
    discord_token = os.environ['DISCORD_TOKEN']
    bot.run(discord_token)

