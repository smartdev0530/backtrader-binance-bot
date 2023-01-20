import os

PRODUCTION = "production"
DEVELOPMENT = "development"

COIN_TARGET = "BTC"
COIN_REFER = "BUSD"

ENV = os.getenv("ENVIRONMENT", PRODUCTION)
DEBUG = False

# BINANCE ACCOUNT INFO
# You have to allow your api key to trade on spot in binance setting
BINANCE = {
    "key": "YOUR KEY",
    "secret": "YOUR SECRET"
}

TELEGRAM = {
    "channel": "<CHANEL ID>",
    "bot": "<BOT KEY HERE>"
}

print("ENV = ", ENV)
