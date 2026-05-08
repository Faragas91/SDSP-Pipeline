import os
import shutil
import pandas as pd
from config.loadConfig import loadConfig

# Function to parse the RNAz file
def parse_petfold_file(file_path):
    
    # Read every line in the .txt file
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith("Score"):
                score = line.split()[-1]
    return {"Score": score}

# All data
def createExcelData(data, count, nameOfFile, excelName):
    for file_name in os.listdir(directory):
        if file_name.startswith(nameOfFile):
            collectDataFromPrediction(data, count, file_name)
        if nameOfFile == "native" and not file_name.startswith("neg_sample"):
            collectDataFromPrediction(data, count, file_name)

    df = pd.DataFrame(data)
    df.to_excel(f"{excelName}.xlsx", index=False)

    print(f"Your data was succsessfully transfered to {excelName}.xlsx.")
    shutil.move(f"/mnt/bernhard/SDSP-Pipeline/{excelName}.xlsx", f"{excel_directory}/{excelName}.xlsx")
    return count 

def collectDataFromPrediction(data, count, file_name):
    count += 1
    print(f"Process file {count}: {file_name}")
    file_path = os.path.join(directory, file_name)
    file_data = parse_petfold_file(file_path)
    file_data["File"] = file_name  
    data.append(file_data)

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)
        
directory = config.get("PETFOLDPREOUTPUT")
excel_directory = config.get("PETFOLDEXCEL")
excel_name = config.get("EXCELNAME")

if (excel_name == "sissi"):
    startname = "pos_sample"
else: 
    startname = "native"

os.makedirs(excel_directory, exist_ok=True)

count = 0
sissi_pos_data = []
count = createExcelData(sissi_pos_data, count, startname, excel_name)

count = 0
alifoldz_data = []
count = createExcelData(alifoldz_data, count, "neg_sample_ALNSHUFFLE", "alnshuffle")

count = 0
multiperm_mono_data = []
count = createExcelData(multiperm_mono_data, count, "neg_sample_MULTIPERM_none", "multiperm_none")

count = 0
multiperm_di_data = []
count = createExcelData(multiperm_di_data, count, "neg_sample_MULTIPERM_level1", "multiperm_level1")

count = 0
sissiz_mono_data = []
count = createExcelData(sissiz_mono_data, count, "neg_sample_SISSIz_mono", "sissiz_mono")

count = 0
sissiz_di_data = []
count = createExcelData(sissiz_di_data, count, "neg_sample_SISSIz_di", "sissiz_di")