import yaml
import pandas as pd
import glob
import os


##Folder for extract data or yaml file stored##
input_folder = "data"
##Folder can save the csv file##
output_folder= "yaml_csv_output"
##Create output folder if it doesn't exist##
os.makedirs(output_folder,exist_ok=True)

##final combine file##
combined_output = os.path.join(output_folder,"all_data.csv")

##Find all yaml files and subfolders too##
yaml_files = glob.glob(os.path.join(input_folder,"**/*.yaml"),recursive=True)
yaml_files += glob.glob(os.path.join(input_folder,"**/*.yaml"),recursive=True)

##List all data and hold it in##
all_datastock = []

for input_path in yaml_files:
    filename= os.path.basename(input_path)
    output_path= os.path.join(output_folder,filename.replace(".yaml",".csv").replace(".yml",".csv"))
    

## Read every yaml file##
    with open(input_path,"r") as file:
        data = yaml.safe_load(file)

##Convert all datastock into DataFrame ##
    df = pd.DataFrame(data)
    all_datastock.append(df) 

    ## Remove time from date column ##
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"],errors = "coerce")
    
##Convert DataFrame into CSV file ##
    df.to_csv(output_path,index=False) 
    print(f"Converted:{output_path}") 

## Combine all datastocks into one CSV file ##
final_df = pd.concat(all_datastock,ignore_index=True)

##Save the combined file ##
final_df.to_csv(combined_output,index=False)
print(f"\n All YAML files are converted successfully")
print(f"Combined file saved as :{combined_output}")

