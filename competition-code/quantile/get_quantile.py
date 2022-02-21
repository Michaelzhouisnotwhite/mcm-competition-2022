# %%
import pandas as pd
import numpy as np

# %%
gen_table = pd.read_csv('../general_table.csv')

# %%
price_table = gen_table[gen_table.columns[1:3]].copy(deep=True)
gold_price = price_table[price_table.columns[0]].copy(deep=True)
bit_price = price_table[price_table.columns[1]].copy(deep=True)

gold_price.plot()
plt.show()
bit_price.plot()
plt.show()
# %%


def get_quantiles(table: pd.Series):
    res_values = np.zeros_like(table.values)
    for i in range(table.index.stop):
        present = table.iloc[i]
        previous = table.iloc[:i + 1].copy(deep=True).drop_duplicates().reset_index(drop=True)
        sorted = previous.sort_values(ascending=True).reset_index(drop=False)
        sorted_index = sorted[sorted[table.name] == present].index.to_numpy()
        max_index = sorted.index.stop

        quantile = (sorted_index) / (max_index -1)

        res_values[i] = quantile

    return res_values.copy()

q1 = get_quantiles(gold_price)
q2 = get_quantiles(bit_price)

# %%
res_df = pd.DataFrame(np.array([q1, q2]).reshape(
    (gold_price.shape[0], 2)), columns=['gold_quantile', 'bit_quantile'])
import pylab as plt
plt.figure()
res_df['gold_quantile'].plot()
plt.show()
res_df['bit_quantile'].plot()
plt.show()
# %%


# %%
gen_table[res_df.columns[0]] = res_df[res_df.columns[0]]
gen_table[res_df.columns[1]] = res_df[res_df.columns[1]]
# %%
gen_table.to_csv("../general_table.csv", index=False)
# %%
