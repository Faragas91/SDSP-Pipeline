import os
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
import time
import threading
from config.loadConfig import loadConfig

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)
# Define variables

ENV = os.environ.copy()
ENV["PETFOLDBIN"] = config.get("PETFOLD")

SAMPLESFASTA = config.get("SAMPLESFASTA")
PETFOLD = config.get("PETFOLD")
PETFOLDPREOUTPUT = config.get("PETFOLDPREOUTPUT")
PETFOLDLOG = config.get("PETFOLDLOG")
NUMCORES = int(config.get("NUMCORES"))   # Number of CPU cores to use

# Create the output directories if they don't exist
os.makedirs(PETFOLDPREOUTPUT, exist_ok=True)

# Function to run a command and return the output
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, env=ENV)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}\n{stderr}")
    return stdout

def process_file_PETfold(file):
    basename = os.path.splitext(file)[0]
    output_file = os.path.join(PETFOLDPREOUTPUT, f"{basename}.txt")
        
    # Check if output file already exists
    if os.path.isfile(output_file):
        print(f"{output_file} already exists, skipping...")
    else:
        # Run PETfold prediction
        run_command(f"{PETFOLD}/PETfold -f {os.path.join(SAMPLESFASTA, file)} >> {output_file}")
        #run_command(f"{PETFOLD} --sci {os.path.join(SAMPLESMAF, file)} >> {output_file}")
        print(f"{output_file} finished")

# Start time measurement
start_time = time.time()
start_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))
print(f"Script started at: {start_time_str}")

count = 0
lock = threading.Lock()

def increment_count():
    global count, start_time
    with lock:
        count += 1
        if count % 1000 == 0:
            elapsed_time = time.time() - start_time
            print(f"Processed {count} files in {elapsed_time:.2f} seconds")
            with open(PETFOLDLOG + "petfold_execution_time.log", "a") as log_file:
                log_file.write(f"Processed {count} files in {elapsed_time:.2f} seconds\n")

# Run PETfold predictions for all samples in parallel
with ProcessPoolExecutor(max_workers=NUMCORES) as executor:
    futures = {executor.submit(process_file_PETfold, file): file for file in os.listdir(SAMPLESFASTA) if file.endswith(".fasta")}
    #futures = {executor.submit(process_file_PETfold, file): file for file in os.listdir(SAMPLESMAF) if file.endswith(".maf")}
    for future in as_completed(futures):
        future.result()
        increment_count()

print("\nProcessing completed.")

# End time measurement
end_time = time.time()
end_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))
execution_time = end_time - start_time

print(f"\nScript finished at: {end_time_str}")
print(f"Total execution time: {execution_time:.2f} seconds")

# Save final execution time to file
with open(PETFOLDLOG + "petfold_execution_time.log", "a") as log_file:
    log_file.write(f"\nScript finished at: {end_time_str}\n")
    log_file.write(f"Total execution time: {execution_time:.2f} seconds\n")
