import pandas as pd
test = pd.read_csv("exchange_rate.csv")
for curr,rate in test.values:
    test[f"MC_{curr}_Billion"] = 100*rate
print(test)
