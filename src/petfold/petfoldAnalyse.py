import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, auc, accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import metrics
import os
from config.loadConfig import loadConfig

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)

PETFOLDEXCEL = config.get("PETFOLDEXCEL")
PETFOLDSAVEPATH = config.get("PETFOLDSAVEPATH")
EXCELNAME = config.get("EXCELNAME")

if not os.path.exists(PETFOLDSAVEPATH):
    os.makedirs(PETFOLDSAVEPATH)

df_positive= pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/{EXCELNAME}.xlsx").dropna())
df_sissiz_mono = pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/sissiz_mono.xlsx").dropna())
df_sissiz_di = pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/sissiz_di.xlsx").dropna())
df_multiperm_none = pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/multiperm_none.xlsx").dropna())
df_multiperm_level1 = pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/multiperm_level1.xlsx").dropna())
df_aln_shuffle = pd.DataFrame(pd.read_excel(f"{PETFOLDEXCEL}/alnshuffle.xlsx").dropna())

dataframes = [df_positive, df_sissiz_mono, df_sissiz_di, df_multiperm_none, df_multiperm_level1, df_aln_shuffle]
labels = [f'{EXCELNAME.upper()}', 'SISSIz_mono', 'SISSIz_di', 'Multiperm_none', 'Multiperm_level1', 'aln-shuffle']
data = [df['Score'] for df in dataframes]
thresholds = [0.5]

plt.figure(figsize=(12, 8))
plt.boxplot(data, labels=labels)

for t in thresholds:
    plt.axhline(y=t, color='red', linestyle='--', linewidth=1)

# Bereiche farbig markieren
plt.axvspan(0.5, 1.5, color="darkgray", alpha=0.75, edgecolor="black", label='Positive Samples')
plt.axvspan(1.5, 3.5, color="sandybrown", alpha=0.75, edgecolor="black", label='Simulation')
plt.axvspan(3.5, 6.5, color="mediumpurple", alpha=0.75, edgecolor="black", label='Shuffle')

# Speichern optional
if PETFOLDSAVEPATH:
    filename = os.path.join(PETFOLDSAVEPATH, f"PETfold: Boxplot Score with randomized samples.png")
    plt.savefig(filename, dpi=300, bbox_inches='tight')

# plt.ylim(0.9825, 1.0)
# plt.title('PETfold: Boxplot Score with randomized samples')
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('legend', fontsize=14)
plt.legend()
plt.close()

