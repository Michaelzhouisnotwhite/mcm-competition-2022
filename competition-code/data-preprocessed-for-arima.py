import pandas as pd
import numpy as np

da = pd.read_csv("./../competition-sources/BCHAIN-MKPRU.csv")

list = da.values.tolist()

for i in range(len(list)-1):
    data = []
    for j in range(i):
        data.append(list[j])

np.save("bit-arima-dataset.npy", np.array(data))
'''
da=pd.read_csv("LBMA-GOLD.csv")
 
list=da.values.tolist()
f=open("LBMA-GOLDdata.csv",'a')
csv_writer = csv.writer(f)
for i in range(1264):
    data=[]
    for j in range(i):
        data.append(list[j])

    csv_writer.writerow(data)
f.close()
'''
