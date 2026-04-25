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

def plot_columns(columnname):
    dataframes = [df_sissi, df_sissiz_mono, df_sissiz_di, df_multiperm_none, df_multiperm_level1, df_aln_shuffle]
    labels = ['SISSI', 'SISSIz_mono', 'SISSIz_di', 'Multiperm_none', 'Multiperm_level1', 'aln-shuffle']
    data = [df[columnname] for df in dataframes]
    # thresholds = [0.9]

    plt.figure(figsize=(12, 8))
    plt.boxplot(data, labels=labels)

    # for t in thresholds:
    #     plt.axhline(y=t, color='red', linestyle='--', linewidth=1)

    plt.axvspan(0.5, 1.5, color="darkgray", alpha=0.75, edgecolor="black", label='Positive Samples')
    plt.axvspan(1.5, 3.5, color="sandybrown", alpha=0.75, edgecolor="black", label='Simulation')
    plt.axvspan(3.5, 6.5, color="mediumpurple", alpha=0.75, edgecolor="black", label='Shuffle')

    if RNAZSAVEPATH:
        filename = os.path.join(RNAZSAVEPATH, f"RNAz: Boxplot {columnname} with randomized samples")
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    # plt.title(f'RNAz: Boxplot {columnname} with randomized samples')
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    plt.rc('legend', fontsize=14)
    plt.legend()
    plt.close()

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)

RNAZEXCEL = config.get("RNAZEXCEL")
RNAZSAVEPATH = config.get("RNAZSAVEPATH")

if not os.path.exists(RNAZSAVEPATH):
        os.makedirs(RNAZSAVEPATH)

df_sissi = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/sissi.xlsx"))
df_sissiz_mono = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/sissiz_mono.xlsx"))
df_sissiz_di = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/sissiz_di.xlsx"))
df_multiperm_none = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/multiperm_none.xlsx"))
df_multiperm_level1 = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/multiperm_level1.xlsx"))
df_aln_shuffle = pd.DataFrame(pd.read_excel(f"{RNAZEXCEL}/alnshuffle.xlsx"))

plot_columns('SVM RNA-class probability')
plot_columns('Structure conservation index')
plot_columns('Mean z-score')
plot_columns('Consensus MFE')
plot_columns('Mean pairwise identity')

