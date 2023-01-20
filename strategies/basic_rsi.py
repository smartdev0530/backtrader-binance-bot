#!/usr/bin/env python3

import backtrader as bt

from config import ENV, PRODUCTION
from strategies.base import StrategyBase
from termcolor import colored


class BasicRSI(StrategyBase):
    params = dict(period_ema_fast=10, period_ema_slow=100)

    def __init__(self):
        StrategyBase.__init__(self)
        self.log("Using RSI/EMA strategy")

        self.ema_fast = bt.indicators.EMA(period=self.p.period_ema_fast)
        self.ema_slow = bt.indicators.EMA(period=self.p.period_ema_slow)
        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.count = 0

        self.profit = 0

    def update_indicators(self):
        self.profit = 0
        if self.buy_price_close and self.buy_price_close > 0:
            self.profit = (
                float(self.data0.close[0] -
                      self.buy_price_close) / self.buy_price_close
            )

    def next(self):
        self.log(
            colored(
                "Next function: $%.2f. , status = %s"
                % (self.data0.close[0], self.status),
                "green",
            ),
            True,
        )
        self.update_indicators()

        if (
            self.status != "LIVE" and ENV == PRODUCTION
        ):  # waiting for live status in production
            return

        if self.order:  # waiting for pending order
            return
        # simply buy / sell on every turn
        if self.last_operation != "BUY":
            self.long()

        if self.last_operation != "SELL":
            self.short()
            self.count = self.count + 1
