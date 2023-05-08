
EE-Alchemy is a Python-based Discord bot that provides users with real-time information on the stock market. Users can request information on trending stocks, trending market news, trending sectors, Options Data and information on a specific stock. The bot also provides information on upcoming stock earning dates, and tutorials on trading tools and patterns.

Getting Started


Prerequisites
Python 3.6 or higher
Discord API token
Alpaca API credentials


Installation:

Clone the repository to your local machine.
Install the required packages by running the following command:

`pip install -r requirements.txt`

Rename config.example.ini to config.ini and update the Discord and Alpaca API credentials.

Usage:
To run the bot, execute the following command in the root directory of the project:


`python Alchemybot.py`

Once the bot is running, users can call it by typing commands in the Discord chat. Here are some examples of commands that the bot understands:

!trending - returns the top 5 trending stocks
!sector [sector] - returns the top 5 trending stocks in a specific sector
!stock [symbol] - returns information on a specific stock
!earnings [symbol] - returns information on upcoming earnings dates for a specific stock
!favorites [add/remove/list] [symbol] - allows users to add or remove stocks from their favorites list
!help - displays a list of available commands and their usage


License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
This bot was developed using the Discord.py library and the Alpaca API. Special thanks to the developers of these tools for making them available to the community.
