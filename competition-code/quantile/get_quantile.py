# %%
import pandas as pd
import numpy as np

# %%
gen_table = pd.read_csv('../general_table.csv')

# %%
price_table = gen_table[gen_table.columns[1:3]].copy(deep=True)
gold_price = price_table[price_table.columns[0]].copy(deep=True)
bit_price = price_table[price_table.columns[1]].copy(deep=True)
# %%


def get_quantiles(table: pd.Series):
    res_values = np.zeros_like(table.values)
    for i in range(table.index.stop):
        present = table.iloc[i]
        previous = table.iloc[:i + 1].copy(deep=True).drop_duplicates().reset_index(drop=True)
        sorted = previous.sort_values(ascending=True).reset_index(drop=False)
        sorted_index = sorted[sorted[table.name] == present].index
        old_index = sorted[sorted[table.name] == present]['index']

        quantile = (sorted_index) / (old_index)

        res_values[i] = quantile

    return res_values


res_df = pd.DataFrame(np.array([get_quantiles(gold_price), get_quantiles(bit_price)]).reshape(
    (gold_price.shape[0], 2)), columns=['gold_quantile', 'bit_quantile'])

# %%
gen_table[res_df.columns[0]] = res_df[res_df.columns[0]]
gen_table[res_df.columns[1]] = res_df[res_df.columns[1]]
# %%
gen_table.to_csv("../general_table_quantile.csv", index=False)
# %%
