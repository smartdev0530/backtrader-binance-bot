#!/usr/bin/env python3

import backtrader as bt
from datetime import datetime

from config import ENV, PRODUCTION
from strategies.base import StrategyBase
from termcolor import colored


class BasicRSI(StrategyBase):
    params = dict(period_ema_fast=10, period_ema_slow=100)

    def __init__(self):
        StrategyBase.__init__(self)
        # self.log("Using RSI/EMA strategy")

        self.ema_fast = bt.indicators.EMA(period=self.p.period_ema_fast)
        self.ema_slow = bt.indicators.EMA(period=self.p.period_ema_slow)
        self.rsi = bt.indicators.RelativeStrengthIndex()

        self.profit = 0
        self.count = 0

    def update_indicators(self):
        self.profit = 0
        if self.buy_price_close and self.buy_price_close > 0:
            self.profit = (
                float(self.data0.close[0] - self.buy_price_close) / self.buy_price_close
            )

    def next(self):

        # self.log(
        #     colored(
        #         "Next function: close =$%.2f open = %.2f high = %.2f low = %.2f , status = %s"
        #         % (
        #             self.data0.close[0],
        #             self.data0.open[0],
        #             self.data0.high[0],
        #             self.data0.low[0],
        #             self.status,
        #         ),
        #         "green",
        #     ),
        #     True,
        # )
        self.update_indicators()

        if (
            self.status != "LIVE" and ENV == PRODUCTION
        ):  # waiting for live status in production
            return

        time_at_backtrader = datetime.utcnow()
        time_at_binance = self.data0.datetime.datetime()

        self.log(
            colored(
                "Candlestick latency : %s"
                % (str(time_at_backtrader - time_at_binance)),
                "green",
            ),
            True,
        )

        if self.order:  # waiting for pending order
            return

        self.count += 1

        # if (self.count == 2) :

        # stop Loss
        # if self.profit < -0.03:
        #     self.log("STOP LOSS: percentage %.3f %%" % self.profit)
        #     self.short()

        if self.last_operation != "SELL":
            # if self.rsi > 53:
            self.short()

        if self.last_operation != "BUY":
            # if self.rsi < 47 and self.ema_fast > self.ema_slow:
            self.long()
