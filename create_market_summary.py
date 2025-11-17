import pandas as pd 
import os


## Input/Output ##
input_folder = "yaml_csv_output/all_data.csv"
output_dir = "analysis_output"
os.makedirs(output_dir,exist_ok=True)

## Read all csv file ##
df = pd.read_csv("yaml_csv_output/all_data.csv")

print("Rows:",len(df))
print("Unique tickers:",df["Ticker"].nunique())

## Clean Date ##
df["date"] =pd.to_datetime(df["date"],errors="coerce")
df = df.dropna(subset=['date'])

## Daily return ##
df["daily_return"]=df.groupby("Ticker")["close"].pct_change()

## Cumulative Return ##
cumulative = (df.groupby("Ticker")["daily_return"]
              .apply(lambda x:(1 + x.fillna(0)).prod()-1).reset_index(name="cumulative_return")
              .sort_values("cumulative_return",ascending=False)) 

## Volatility (std dev) ##
top_10_volatile=(df.groupby("Ticker")["daily_return"].std().reset_index(name="volatility")
             .sort_values("volatility",ascending=False).head(10))


## correlation matrix  ##
close_pivot = df.pivot_table(index="date",columns="Ticker",values="close")
correlation_matrix = close_pivot.corr()

## Monthly return ##
df["month"] = df["date"].dt.to_period("M").astype(str)
monthly_return = (df.groupby(["Ticker","month"])["close"]
                  .apply(lambda x:(x.iloc[-1]- x.iloc[0])/ x.iloc[0]).reset_index(name="monthly_return"))
top5_month = (monthly_return.sort_values(["month","monthly_return"],ascending=[True,False]).groupby("month").head(5))
bottom5_month = (monthly_return.sort_values(["month","monthly_return"],ascending=[True,True]).groupby("month").head(5))

## Top 10 gainers ##
top_10_gainers= (df.groupby("Ticker")["daily_return"]
                 .apply(lambda x:(1 + x.fillna(0)).prod()-1).sort_values(ascending=False).head(10)
                 .reset_index(name="cumulative_return")) 
                  
## Top 10 losers ##
top_10_losers= (df.groupby("Ticker")["daily_return"]
                 .apply(lambda x:(1 + x.fillna(0)).prod()-1).sort_values(ascending=True).head(10)
                 .reset_index(name="cumulative_return")) 


## Save output files ## 
cumulative.to_csv(os.path.join(output_dir,"cumulative_return.csv"),index=False)
top_10_volatile.to_csv(os.path.join(output_dir,"top_10_volatile.csv"),index=False)
correlation_matrix.to_csv(os.path.join(output_dir,"correlation_matrix.csv"),index=False)
monthly_return.to_csv(os.path.join(output_dir,"monthly_return.csv"),index=False)
top_10_gainers.to_csv(os.path.join(output_dir,"top_10_gainers.csv"),index=False)
top_10_losers.to_csv(os.path.join(output_dir,"top_10_losers.csv"),index=False)
top5_month.to_csv(os.path.join(output_dir,"top5_month.csv"),index=False)
bottom5_month.to_csv(os.path.join(output_dir,"bottom5_month.csv"),index=False)
print("🎊Market summary created successfully!")
