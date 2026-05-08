import os
import shutil
import time
import subprocess
import random
import glob
from config.loadConfig import loadConfig
from pathlib import Path

config_path = os.getenv("CONFIG_FILE")

if not config_path:
    raise ValueError("CONFIG_FILE environment variable is not set. Please set it to the path of the configuration file.")

config = loadConfig(config_path)

TOTAL_FILES = int(config["ITER"]) * 5
SISSIZ = config["SISSIZ"]
MULTIPERM = config["MULTIPERM"]
ALNSHUFFLE = config["ALNSHUFFLE"]
SAMPLESCLUSTAL = config["SAMPLESCLUSTAL"]
ITER = int(config["ITER"])

current_file = 0
# ========================
# Helper Functions
# ========================
def show_progress():
    percentage = int(current_file * 100 / TOTAL_FILES)
    print(f"\rProgress: {percentage}% ({current_file}/{TOTAL_FILES})", end="")


def run_command(cmd, output_file=None):
    with open(output_file, "w") if output_file else subprocess.DEVNULL as out:
        subprocess.run(cmd, shell=True, stdout=out, check=True)


def elapsed(start, last):
    current = time.time()
    diff = current - last
    return current, diff


# ========================
# START
# ========================
os.makedirs(SAMPLESCLUSTAL, exist_ok=True)
NATIVE = Path(SAMPLESCLUSTAL)


# ========================
# SISSIz mono
# ========================
print("\n\nStarted to generate SISSIz mononucleotide samples")
start = time.time()
last_time = start

for file in NATIVE.iterdir():
    if file.name.startswith("neg_sample"):
        continue
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_SISSIz_mono_output_{file.name}"

    if not os.path.exists(OUTPUT):
        cmd = f"{SISSIZ} -s -i {file}"
        run_command(cmd, OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"SISSIz_mono sample {file.name} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nSISSIz_mono runtime: {time.time() - start:.2f} seconds")


# ========================
# SISSIz di
# ========================
print("\nStarted to generate SISSIz dinucleotide samples")
start = time.time()
last_time = start

for file in NATIVE.iterdir():
    if file.name.startswith("neg_sample"):
        continue
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_SISSIz_di_output_{file.name}"

    if not os.path.exists(OUTPUT):
        cmd = f"{SISSIZ} -s {file}"
        run_command(cmd, OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"SISSIz_di sample {file.name} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nSISSIz_di runtime: {time.time() - start:.2f} seconds")


# ========================
# Multiperm none
# ========================
print("\nStarted to generate Multiperm none samples")
start = time.time()
last_time = start

for file in NATIVE.iterdir():
    if file.name.startswith("neg_sample"):
        continue
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_MULTIPERM_none_output_{file.name}"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"{MULTIPERM} -w --conservation=none {file}", shell=True)
        files = glob.glob(f"perm_001_{file.name}")
        if files:
            shutil.move(files[0], OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Multiperm_none sample {file.name} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nMultiperm_none runtime: {time.time() - start:.2f} seconds")


# ========================
# Multiperm level1
# ========================
print("\nStarted to generate Multiperm level1 samples")
start = time.time()
last_time = start

for file in NATIVE.iterdir():
    if file.name.startswith("neg_sample"):
        continue
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_MULTIPERM_level1_output_{file.name}"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"{MULTIPERM} -w {file}", shell=True)
        files = glob.glob(f"perm_001_{file.name}")
        if files:
            shutil.move(files[0], OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Multiperm_level1 sample {file.name} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nMultiperm_level1 runtime: {time.time() - start:.2f} seconds")


# ========================
# Alnshuffle
# ========================
print("\nStarted to generate Alnshuffle samples")
start = time.time()
last_time = start

for file in NATIVE.iterdir():
    if file.name.startswith("neg_sample"):
        continue
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_ALNSHUFFLE_output_{file.name}"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"perl {ALNSHUFFLE} < {file} > {OUTPUT}", shell=True)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Alnshuffle sample {file.name} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\Alnshuffle runtime: {time.time() - start:.2f} seconds")