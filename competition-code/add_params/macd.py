# %%
import pandas as pd
import numpy as np
# %%
gen_data = pd.read_csv('../general_table.csv')

# %%
price_table = gen_data[gen_data.columns[1: 3]].copy(deep=True).values
# %%


def ema_today(n):
    ema_today = np.zeros_like(price_table)
    ema_today[0] = price_table[0]

    alpha = 2 / (n + 1)
    for idx in range(1, price_table.shape[0]):
        ema_today[idx] = price_table[idx]*alpha + ema_today[idx - 1] * (1 - alpha)
    return ema_today


def dif():
    return ema_today(12) - ema_today(26)


def dea():
    dea_values = np.zeros_like(price_table)
    dif_values = dif()
    for i in range(1, dea_values.shape[0]):
        dea_values[i] = dea_values[i - 1] * 8 / 10 + dif_values[i] * 2 / 10
    return dea_values


macd = (dif() - dea()) * 2
# %%
gen_data['gold_macd'] = macd[:, 0]
gen_data['bit_macd'] = macd[:, 1]
gen_data['gold_dif'] = dif()[:, 0]
gen_data['bit_dif'] = dif()[:, 1]
gen_data['gold_dea'] = dea()[:, 0]
gen_data['bit_dea'] = dea()[:, 1]
# %%
gen_data.to_csv("../general_table.csv", index=False)

# %%
