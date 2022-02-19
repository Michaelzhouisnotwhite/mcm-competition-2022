"""
@author: Michael
@Date: 2022-02-18
@Information: 处理数据,表头为:
    [
        'Date', 
        'USD (PM)黄金', 
        'Value比特币', 
        'able_trade_gold是否是黄金交易日', 
        'gold_growth_rate黄金涨幅',
        'bit_growth_rate比特币涨幅', 
        'gip 当前黄金投资占比', 
        'bip 当前比特币投资占比', 
        'gir 黄金投资风险', 
        'bir 比特币投资风险', 
        'C 现金持有份额', 
        'G 黄金持有份额', 
        'B 比特币持有份额',
        'total property 总资产'
    ]

"""
# %%
import numpy as np
import pandas as pd
# %%
gold_data = pd.read_csv(r"./../competition-sources\LBMA-GOLD.csv")
bit_data = pd.read_csv(r"./../competition-sources\BCHAIN-MKPRU.csv")
# %%
general_table_raw_data = pd.merge(gold_data, bit_data, how='outer', on='Date')
# %%


def format_date(date: str):
    assert isinstance(date, str)
    res = date.split('/')
    m, d, y = res[0], res[1], res[2]

    def format_int(x):
        if int(x) < 10:
            return '0{}'.format(x)
        return '{}'.format(x)
    return "20{}-{}-{}".format(y, format_int(m), format_int(d))


general_table_raw_data['Date'] = general_table_raw_data['Date'].apply(format_date)
# %%
general_table_raw_data.sort_values(by=['Date'], ascending=True, inplace=True)
# %%
general_table_raw_data.reset_index(inplace=True, drop=True)
# %%
# %%
general_table_raw_data['able_trade_gold'] = (
    general_table_raw_data.isna()[general_table_raw_data.columns[1]]).apply(lambda x: int(not x))

if pd.isna(general_table_raw_data[general_table_raw_data.columns[1]][0]):
    general_table_raw_data.loc[0, general_table_raw_data.columns[1]
                               ] = general_table_raw_data[general_table_raw_data.columns[1]][1]

# %%
general_table_raw_data.fillna(axis=0, method='ffill', inplace=True)
# %%
increasing_rate_values = [np.array([0, 0])]
target = general_table_raw_data[general_table_raw_data.columns[1:3]].values
for idx in range(1, general_table_raw_data.index.stop):
    def get_increasin_rate(prev, now):
        return (now - prev) / prev
    increasing_rate_values.append(get_increasin_rate(target[idx - 1], target[idx]))

increasing_rate_values = np.array(increasing_rate_values)

# %%
general_table_raw_data = pd.concat([general_table_raw_data, pd.DataFrame(
    increasing_rate_values, columns=['gold_growth_rate', 'bit_growth_rate'], index=None)], axis=1)

# %%
general_table = pd.concat([general_table_raw_data, pd.DataFrame(
    columns=['gip', 'bip', 'gir', 'bir', 'C', 'G', 'B', 'total property'])])
# %%

general_table.to_csv('general_table.csv', index=False)
# %%
