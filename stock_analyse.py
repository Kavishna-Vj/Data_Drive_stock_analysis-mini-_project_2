import streamlit as st 
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import os 

st.set_page_config(page_title="Stock Market Dashboard",layout="wide")

OUTPUT_FOLDER="analysis_output"

def load(file):
    path = os.path.join(OUTPUT_FOLDER,file)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
       None

## Page Tittle ##
st.title("📊Stock Market Analysis")

cumulative=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/cumulative_return.csv")
volatility=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/top_10_volatile.csv")
gainers=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/top_10_gainers.csv")
losers=load("C:/Users/sujit/OneDrive/Desktop\project_2/analysis_output/top_10_losers.csv")
monthly_return=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/monthly_return.csv")
top5_month=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/top5_month.csv")
bottom5_month=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/bottom5_month.csv")
corr_matrix=load("C:/Users/sujit/OneDrive/Desktop/project_2/analysis_output/correlation_matrix.csv")


## Top 10 gainers ##
st.subheader("Top 10 Gainers")
if gainers is not None:
 st.bar_chart(gainers.set_index("Ticker")["cumulative_return"],color="#00C853")
plt.show()

## Top 10 losers ##
st.subheader("Top 10 losers")
if losers is not None:
 st.bar_chart(losers.set_index("Ticker")["cumulative_return"],color="#D50000")
plt.show()

## Top 10 volatile ##
st.subheader("Top 10 volatile")
if volatility is not None:
 st.bar_chart(volatility.set_index("Ticker")["volatility"])
plt.show()

## Correlation Heatmap ##
st.subheader(" Correlation matrix")
if corr_matrix is not None:
  fig, ax = plt.subplots(figsize=(12,8))
  sns.heatmap(corr_matrix,cmap="viridis", ax=ax)
  st.pyplot(fig)

## Monthly Returns ##
st.subheader("Monthly  Returns by Month")

if monthly_return is  None :
      st.error("monthly_return.csv not found! Please check analysis_output_folder.")
else:
      if monthly_return.empty:
         st.warning("monthly_return.csv is empty!")
      else:
       months=sorted(monthly_return["month"].unique())
       month_sel=st.selectbox("Select Month", months) 

       month_df=monthly_return[monthly_return["month"]== month_sel].copy()
       if month_df.empty:
          st.warning(f"No data found for{month_sel}")
       else:
          month_df["color"]=month_df["monthly_return"].apply(lambda x: "green" if x >=0 else "red")

          fig, ax = plt.subplots(figsize=(12,4))
          ax.bar(month_df["Ticker"],month_df["monthly_return"],color=month_df["color"])
          plt.xticks(rotation=90)
          st.pyplot(fig)
      
         
## Top 5 and Botton 5 per month ##
st.subheader("Top 5 & Bottom 5 stocks(Monthly)")

if top5_month is not None and bottom5_month is not None:
  
  months2 = sorted(top5_month["month"].unique())
  month_pick = st.selectbox("Select Month For Top/Bottom 5", months2)

  ## Top 5 ##
top5_month= top5_month[top5_month["month"]==month_pick]
fig, ax = plt.subplots(figsize=(12,10))
ax.bar(top5_month["Ticker"],top5_month["monthly_return"],color="green")
plt.xticks(rotation=90)
st.pyplot(fig)

  ## Bottom 5 ##
bottom5_month= bottom5_month[bottom5_month["month"]==month_pick]
fig, ax = plt.subplots(figsize=(12,10))
ax.bar(bottom5_month["Ticker"],bottom5_month["monthly_return"],color="red")
plt.xticks(rotation=90)
st.pyplot(fig)

st.success("Dashboard Loaded Successfully")