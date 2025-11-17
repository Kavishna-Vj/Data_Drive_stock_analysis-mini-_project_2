import pandas as pd

## Read CSV file ##
df = pd.read_csv("yaml_csv_output/all_data.csv")

##Group by tickers and save the tickers as seperated csv files ##
for symbol, group in df.groupby('Ticker'):
    group.to_csv(f'{symbol}_data.csv',index=False)