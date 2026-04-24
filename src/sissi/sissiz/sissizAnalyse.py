import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix, auc, accuracy_score,  classification_report, precision_recall_curve, ConfusionMatrixDisplay
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn import metrics
from sklearn.calibration import calibration_curve
import os
from config.loadConfig import loadConfig

def plot_columns(columnname, thresholds):
    dataframes = [df_sissi, df_sissiz_mono , df_sissiz_di, df_multiperm_none, df_multiperm_level1, df_aln_shuffle]
    labels = ['SISSI', 'SISSIz_mono', 'SISSIz_di', 'Multiperm_none', 'Multiperm_level1', 'aln-shuffle']
    data = [df[columnname] for df in dataframes]

    plt.figure(figsize=(12, 8))
    plt.boxplot(data, labels=labels)

    if thresholds == None:
        thresholds = []
    else:
        for t in thresholds:
            plt.axhline(y=t, color='red', linestyle='--', linewidth=1, label=f'Threshold {t}')

    plt.axvspan(0.5, 1.5, color="darkgray", alpha=0.75, edgecolor="black", label='Positive Samples')
    plt.axvspan(1.5, 3.5, color="sandybrown", alpha=0.75, edgecolor="black", label='Simulation')
    plt.axvspan(3.5, 6.5, color="mediumpurple", alpha=0.75, edgecolor="black", label='Shuffle')

    if SISSIZSAVEPATH:
        filename = os.path.join(SISSIZSAVEPATH, f"SISSIz: Boxplot {columnname} with randomized samples")
        plt.savefig(filename, dpi=300, bbox_inches='tight')

    # plt.ylim(0.0, 1.0)
    # plt.title(f'SISSIz: Boxplot {columnname}')
    plt.rc('xtick', labelsize=12)
    plt.rc('ytick', labelsize=12)
    plt.rc('legend', fontsize=14)
    plt.legend()
    plt.show()

config = loadConfig("config/pipeline.conf")

SISSIZEXCEL = config.get("SISSIZEXCEL")
SISSIZSAVEPATH = config.get("SISSIZSAVEPATH")

if not os.path.exists(SISSIZSAVEPATH):
    os.makedirs(SISSIZSAVEPATH)

df_sissi = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/sissi.xlsx"))
df_sissiz_mono = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/sissiz_mono.xlsx"))
df_sissiz_di = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/sissiz_di.xlsx"))
df_multiperm_none = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/multiperm_none.xlsx"))
df_multiperm_level1 = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/multiperm_level1.xlsx"))
df_aln_shuffle = pd.DataFrame(pd.read_excel(f"{SISSIZEXCEL}/alnshuffle.xlsx"))
 
plot_columns('Mean Pairwise Identity (MPI) of the input alignment', None)
plot_columns('Average MPI of the sampled alignments', None)
plot_columns('Standard deviation of the MPIs of the sampled alignments', None)
plot_columns('Structural Conservation Index (SCI)', None)
plot_columns('GC-Content', None)
plot_columns('RNAalifold consensus Minimum Free Energy (MFE) of the original alignment', None)
plot_columns('Average consensus MFE in the sampled alignments', None)
plot_columns('Standard deviation of the consensus MFE in the sampled alignments', None)
plot_columns('z-score calculated from 7 8 and 9', [-4, 4])

