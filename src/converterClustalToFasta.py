import os
from Bio import SeqIO
from config.loadConfig import loadConfig

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)

SAMPLESCLUSTAL = config["SAMPLESCLUSTAL"]
SAMPLESFASTA = config["SAMPLESFASTA"]

if not os.path.exists(SAMPLESFASTA):
    os.makedirs(SAMPLESFASTA)

def convertClustalToFasta(inputDir):
    for file in os.listdir(inputDir):
        if file.endswith(".clu"):
            input_file_path = os.path.join(inputDir, file)
            output_file_path = os.path.join(SAMPLESFASTA, os.path.splitext(file)[0] + ".fasta")
            
            try:
                with open(input_file_path, "r") as input_file:
                    records = SeqIO.parse(input_file, "clustal")
                    count = SeqIO.write(records, output_file_path, "fasta")
                    print(f"Converted {count} records from {file} to {output_file_path}")
            except Exception as e:
                print(f"Error processing file {file}: {e}")

convertClustalToFasta(SAMPLESCLUSTAL)
