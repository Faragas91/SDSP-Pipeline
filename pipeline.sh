#!/bin/bash
MODE=${1:-sissi}

if [[ "$MODE" != "native" && "$MODE" != "sissi" && "$MODE" != "both" ]]; then
    echo "Usage: $0 [native|sissi|both]"
    exit 1
fi

export PYTHONPATH="$(pwd):$PYTHONPATH"

##################################
# Funktion
##################################
run_pipeline () {
    MODE_NAME=$1

    echo "Running pipeline in $MODE_NAME mode"

    export CONFIG_FILE="config/pipeline_${MODE_NAME}.conf"

    # python src/converterClustalToFasta.py
    # python src/sissiz/sissizPrediction.py
    # python src/rnaz/rnazPrediction.py
    # python src/petfold/petfoldPrediction.py

    # python src/sissiz/transferSISSIzDataToExcel.py
    # python src/rnaz/transferRNAzDataToExcel.py
    # python src/petfold/transferPETfoldDataToExcel.py

    python src/sissiz/sissizAnalyse.py
    python src/rnaz/rnazAnalyse.py
    python src/petfold/petfoldAnalyse.py

    python src/sissiz/sissizRocCurve.py
    python src/rnaz/rnazRocCurve.py
    python src/petfold/petfoldRocCurve.py
}

##################################
# Aufruf
##################################
if [[ "$MODE" == "native" || "$MODE" == "both" ]]; then
    run_pipeline native
fi

if [[ "$MODE" == "sissi" || "$MODE" == "both" ]]; then
    run_pipeline sissi
fi