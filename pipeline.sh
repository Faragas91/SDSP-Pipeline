#!/bin/bash
MODE=${1:-sissi}

if [[ "$MODE" != "native" && "$MODE" != "sissi" ]]; then
    echo "Usage: $0 [native|sissi]"
    exit 1
fi

echo "Set up the tool paths by sourcing the config file"
source config/pipeline.conf

export PYTHONPATH="$(pwd):$PYTHONPATH"

if [[ "$MODE" == "native" ]]; then
    echo "Running the pipeline in native mode"

    echo "Starting to destroy the native samples"
    python src/native/NativeDestruction.py
    echo "Finished destroying the native samples"

    echo "Transform the CLUSTAL files to FASTA format for PETfold"
    python src/native/convertClustalToFasta.py
    echo "Finished transforming the CLUSTAL files to FASTA format for PETfold"

    echo "Started the prediction of the randomized and native samples"
    python src/native/Structure_prediction.py
    echo "Finished the prediction of the randomized and native samples"

    echo "Transfer the results into excel files for further analysis"
    python src/native/transferPredictionResults.py
    echo "Finished transferring the results into excel files for further analysis"

    echo "Generate the plots for the analysis"
    python src/native/plotResults.py
    echo "Finished generating the plots for the analysis"

    echo "Finished the pipeline"

elif [[ "$MODE" == "sissi" ]]; then
    echo "Running the pipeline in sissi mode"

    echo "Starting to generate the randomized samples"
    python src/sissi/sampleGeneratorForSISSI.py
    echo "Finished generating randomized samples"

    echo "Transform the CLUSTAL files to FASTA format for PETfold"
    python src/sissi/converterClustalToFasta.py
    echo "Finished transforming the CLUSTAL files to FASTA format for PETfold"

    echo "Started the prediction of the randomized and native samples"
    python src/sissi/sissiz/sissizPrediction.py
    python src/sissi/rnaz/rnazPrediction.py
    python src/sissi/petfold/petfoldPrediction.py
    echo "Finished the prediction of the randomized and native samples"

    echo "Transfer the results into excel files for further analysis"
    python src/sissi/sissiz/transferSISSIzDataToExcel.py
    python src/sissi/rnaz/transferRNAzDataToExcel.py
    python src/sissi/petfold/transferPETfoldDataToExcel.py
    echo "Finished transferring the results into excel files for further analysis"

    echo "Analyze the results"
    python "src/sissi/sissiz/sissizAnalyse.py"
    python "src/sissi/rnaz/rnazAnalyse.py"
    python "src/sissi/petfold/petfoldAnalyse.py"
    echo "Finished analyzing the results"

    echo "Generate ROC curves for the analysis"
    python src/sissi/sissiz/sissizRocCurve.py
    python src/sissi/rnaz/rnazRocCurve.py
    python src/sissi/petfold/petfoldRocCurve.py
    echo "Finished generating ROC curves for the analysis"

    echo "Finished the pipeline"
fi











