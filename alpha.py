import os
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np


def ema(x, a, adjust=False):
    return x.ewm(alpha=a, adjust=adjust).mean()


def ts_rank(s, window):
    s = s.dropna()

    rankings = s.rolling(window).apply(
        lambda x: np.searchsorted(np.sort(x), x.iloc[-1]) + 1
    )

    return (rankings - 1) / (window - 1)


def parse_tsrank(data, ema_alpha, ts_rank_w):
    data = ema(data, ema_alpha)
    data = ts_rank(data, ts_rank_w) - 0.5
    factor = data / data.abs()
    factor = factor.replace(np.nan, 0)
    return factor


def parse_diff(data, ema_alpha, diff_w):
    data = ema(data, ema_alpha)
    data = data.diff(diff_w)
    factor = data / data.abs()
    factor = factor.replace(np.nan, 0)
    return factor


def alpha(self, quote):
    auto_export = getDF(quote, "auto")["I_S009065219"].fillna(method="ffill")
    house_price = getDF(quote, "real_estate")["I_S004543083"].fillna(method="ffill")
    heat_pump = getDF(quote, "mech_equip")["I_S006699504"].fillna(method="ffill")
    const_mech = getDF(quote, "mech_equip")["I_S005951771"].fillna(method="ffill")
    loco_yield = getDF(quote, "arch_dec")["I_M001622745"].fillna(method="ffill")

    f_auto_export = parse_tsrank(auto_export, ema_alpha=1 / 3, ts_rank_w=9)
    f_house_price = parse_tsrank(house_price, ema_alpha=1 / 2, ts_rank_w=30)
    f_heat_pump = parse_diff(heat_pump, ema_alpha=1 / 85, diff_w=15)
    f_const_mech = parse_tsrank(const_mech, ema_alpha=1 / 45, ts_rank_w=15)
    f_loco_yield = parse_tsrank(loco_yield, ema_alpha=1 / 10, ts_rank_w=150)

    factors = pd.concat(
        [f_auto_export, f_house_price, f_heat_pump, f_const_mech, f_loco_yield], axis=1
    )

    factors_sum = factors.sum(axis=1)
    alpha = factors_sum / factors_sum.abs()
    alpha = alpha.replace(np.nan, 0)

    alpha = alpha.loc["2015-01-01":]

    return alpha


def getDF(quote, name):
    path = os.path.join(quote, name + ".csv")
    return pd.read_csv(path, index_col=0, parse_dates=True)


if __name__ == "__main__":
    quote = "C:/Users/ifwha/OneDrive - CUHK-Shenzhen/桌面/工作/A04_指数编制/quote/QUOTE_INDUSTRY/assembler"
    plt.plot(alpha(None, quote))
    plt.show()