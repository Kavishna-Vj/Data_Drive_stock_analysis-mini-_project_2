import pandas as pd 
import os 

input_folder = "all_data.csv"
output_dir = "analysis_output"
os.makedirs(output_dir,exist_ok=True)

df = pd.read_csv(input_folder)
print("Column in CSV:",df.columns.tolist())

df.columns = [c.strip() for c in df.columns]
df['date']=pd.to_datetime(df['Date'],errors ='coerce')
df = df.dropna(subset=['Ticker','Date','Close'])
## calculate  return and volatility#
df['Daily Return'] = df.groupby('Ticker')['Close'].pct_change()
summary = df.groupby('Ticker').agg(Cumulative_return=('Daily Return',lambda x: (1+x).prod()-1),
                                   Volatility =('Daily Return','std'),
                                   Avg_Price=('Close','mean'),
                                   Avg_Volume=('vol_col','mean')).reset_index()
## Save analysis output ##
summary.to_csv(f"{output_dir}/market_summary.csv", index=False)
print("Market summary created successfully")