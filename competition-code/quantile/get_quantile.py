# %%
import pandas as pd
import numpy as np

# %%
gold_data = pd.read_csv("./LBMA-GOLD.csv")
print(gold_data.columns)

# %%


def get_present_quantile(idx):
    present_data = gold_data.iloc[idx, :]
    previous_data = gold_data.iloc[: idx + 1, :]
    asce_data = previous_data.sort_values(by=[gold_data.columns[1]],
                                          ascending=True).reset_index(drop=True).copy(deep=True)
    quantile = asce_data[asce_data['Date'] == present_data.values[0]].index / idx
    return quantile


# %%
res = []
for idx in range(gold_data.index.stop):
    quantile = get_present_quantile(idx)
    res.append(quantile)

# %%

res_df = pd.DataFrame(np.concatenate((gold_data.iloc[:, 0].values.reshape(
    gold_data.iloc[:, 0].values.shape[0], 1), np.array(res)), axis=1), columns=gold_data.columns)
# %%
res_df.to_csv('quantile_value.csv', index=False)
# with pd.ExcelWriter("./quantile_value.xlsx") as f:
#     res_df.to_excel(f, index=False)

# # %%
# with pd.ExcelWriter("./LBMA-GOLD.xlsx") as f:
#     gold_data.to_excel(f, index=False)
