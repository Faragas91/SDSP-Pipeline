import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
        confusion_matrix,
        classification_report,
        roc_curve,
        auc,
        accuracy_score,
        precision_score,
        recall_score,
        f1_score
    )
import os
from config.loadConfig import loadConfig

def evaluate_classifier(
    df_positive,
    df_negative,
    pos_label=1,
    neg_label=0,
    title_suffix="",
    save_path=None
):


    # ----------------------------
    # Prepare data
    # ----------------------------
    df_positive = df_positive.copy()
    df_negative = df_negative.copy()

    df_positive["Label"] = pos_label
    df_negative["Label"] = neg_label

    data = pd.concat([df_positive, df_negative], ignore_index=True)

    X = data[["z-score calculated from 7 8 and 9"]]
    y = data["Label"]

    # ----------------------------
    # Histogram
    # ----------------------------
    plt.figure(figsize=(12, 8))
    sns.histplot(
        data=data,
        x="z-score calculated from 7 8 and 9",
        hue="Label",
        bins=50,
        kde=True
    )
    plt.xlabel("z-score calculated from 7 8 and 9")
    plt.ylabel("Count")
    plt.legend(["Negative", "Positive"])
    plt.tight_layout()

    if SISSIZSAVEPATH:
        plt.savefig(
            os.path.join(SISSIZSAVEPATH, f"SISSIz: Histogram {title_suffix}.png"),
            dpi=300,
            bbox_inches="tight"
        )
    plt.close()

    # ----------------------------
    # Logistic Regression with CV
    # ----------------------------
    model = LogisticRegression(
        max_iter=1000,
        class_weight="balanced",
        solver="lbfgs"
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    y_pred = cross_val_predict(
        model,
        X,
        y,
        cv=cv,
        method="predict"
    )

    y_proba = cross_val_predict(
        model,
        X,
        y,
        cv=cv,
        method="predict_proba"
    )[:, 1]

    # ----------------------------
    # Confusion Matrix
    # ----------------------------
    cm = confusion_matrix(y, y_pred)

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["Negative", "Positive"],
        yticklabels=["Negative", "Positive"]
    )
    plt.xlabel("Predicted label")
    plt.ylabel("True label")
    plt.tight_layout()

    if SISSIZSAVEPATH:
        plt.savefig(
            os.path.join(SISSIZSAVEPATH, f"SISSIz: Confusion Matrix {title_suffix}.png"),
            dpi=300,
            bbox_inches="tight"
        )
    plt.close()

    print("\nClassification report:\n")
    print(classification_report(y, y_pred))

    # ----------------------------
    # ROC Curve
    # ----------------------------
    fpr, tpr, _ = roc_curve(y, y_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(12, 8))
    plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], "--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.tight_layout()

    if SISSIZSAVEPATH:
        plt.savefig(
            os.path.join(SISSIZSAVEPATH, f"SISSIz: ROC {title_suffix}.png"),
            dpi=300,
            bbox_inches="tight"
        )
    plt.close()

    # ----------------------------
    # Metrics
    # ----------------------------
    print(f"AUC:       {roc_auc:.4f}")
    print(f"Accuracy:  {accuracy_score(y, y_pred):.4f}")
    print(f"Precision: {precision_score(y, y_pred):.4f}")
    print(f"Recall:    {recall_score(y, y_pred):.4f}")
    print(f"F1-score:  {f1_score(y, y_pred):.4f}")

    return {
        "label": title_suffix,
        "y_true": y,
        "y_proba": y_proba,
        # "model": "Logistic Regression"
    }

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)

SISSIZEXCEL = config.get("SISSIZEXCEL")
SISSIZSAVEPATH = config.get("SISSIZSAVEPATH")

if not os.path.exists(SISSIZSAVEPATH):
    os.makedirs(SISSIZSAVEPATH)

# Load the data
df_sissi = pd.read_excel(f"{SISSIZEXCEL}/sissi.xlsx", usecols=['z-score calculated from 7 8 and 9'])
df_sissiz_mono = pd.read_excel(f"{SISSIZEXCEL}/sissiz_mono.xlsx", usecols=['z-score calculated from 7 8 and 9'])
df_sissiz_di = pd.read_excel(f"{SISSIZEXCEL}/sissiz_di.xlsx", usecols=['z-score calculated from 7 8 and 9'])
df_multiperm_none = pd.read_excel(f"{SISSIZEXCEL}/multiperm_none.xlsx", usecols=['z-score calculated from 7 8 and 9'])
df_multiperm_level1 = pd.read_excel(f"{SISSIZEXCEL}/multiperm_level1.xlsx", usecols=['z-score calculated from 7 8 and 9'])
df_aln_shuffle = pd.read_excel(f"{SISSIZEXCEL}/alnshuffle.xlsx", usecols=['z-score calculated from 7 8 and 9'])


all_roc_data = []

tools = [
    {
        "df_positive": df_sissi,
        "df_negative": df_sissiz_mono,
        "title_suffix": "SISSI vs SISSIz_MONO with randomized samples",
        "save_path": SISSIZSAVEPATH
    }, 
    {
        "df_positive": df_sissi,
        "df_negative": df_sissiz_di,
        "title_suffix": "SISSI vs SISSIz_DI with randomized samples",
        "save_path": SISSIZSAVEPATH
    }, 
    {
        "df_positive": df_sissi,
        "df_negative": df_multiperm_none,
        "title_suffix": "SISSI vs Multiperm_NONE with randomized samples",
        "save_path": SISSIZSAVEPATH
    }, 
    {
        "df_positive": df_sissi,
        "df_negative": df_multiperm_level1,
        "title_suffix": "SISSI vs Multiperm_LEVEL1 with randomized samples",
        "save_path": SISSIZSAVEPATH
    }, 
    {
        "df_positive": df_sissi,
        "df_negative": df_aln_shuffle,
        "title_suffix": "SISSI vs Aln_Shuffle with randomized samples",
        "save_path": SISSIZSAVEPATH
    }
]

for tool in tools:
    roc_data = evaluate_classifier(
        df_positive=tool["df_positive"],
        df_negative=tool["df_negative"],
        title_suffix=tool["title_suffix"],
        save_path=tool["save_path"]
    )
    all_roc_data.append(roc_data)

plt.figure(figsize=(12, 8))

for entry in all_roc_data:
    fpr, tpr, _ = roc_curve(entry['y_true'], entry['y_proba'])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label=f"{entry['label']} (AUC = {roc_auc:.2f})")

plt.plot([0, 1], [0, 1], 'k--', label='Random')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.rc('axes', labelsize=14)
plt.rc('xtick', labelsize=14)
plt.rc('ytick', labelsize=14)
plt.rc('legend', fontsize=14)
# plt.title("SISSIz: ROC-Curves Comparison with randomized samples")
plt.legend(loc="lower right")
plt.grid(True)
plt.tight_layout()
if SISSIZSAVEPATH:
    filename = os.path.join(SISSIZSAVEPATH, "SISSIz: ROC Curve All with randomized samples.png")
    plt.savefig(filename, dpi=300, bbox_inches='tight')
plt.close()

