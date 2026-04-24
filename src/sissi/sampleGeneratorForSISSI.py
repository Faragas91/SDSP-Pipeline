import os
import time
import subprocess
import random
import glob
from config.loadConfig import loadConfig

config = loadConfig("config/pipeline.conf")

TOTAL_FILES = int(config["ITER"]) * 6
SISSI = config["SISSI"]
SISSIZ = config["SISSIZ"]
MULTIPERM = config["MULTIPERM"]
ALNSHUFFLE = config["ALNSHUFFLE"]
FREQUENCIES_SINGLE = config["FREQUENCIES_SINGLE"]
FREQUENCIES_DOUBLE = config["FREQUENCIES_DOUBLE"]
NEIGHBOURHOOD = config["NEIGHBOURHOOD"]
TREE = config["TREE"]
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

print("\nStarted to generate SISSI samples")
start_sissi = time.time()
last_time = start_sissi


for i in range(1, ITER + 1):

    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{i}.clu"

    if not os.path.exists(SISSI_OUTPUT):
        cmd = f"{SISSI} -fs {FREQUENCIES_SINGLE} -fd {FREQUENCIES_DOUBLE} -nn {NEIGHBOURHOOD} -l401 {TREE} -oc"
        run_command(cmd, SISSI_OUTPUT)
        time.sleep(random.uniform(1, 2))
        print("SISSI finished")
    else:
        print(f"{SISSI_OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start_sissi, last_time)
    print(f"SISSI sample {i} took {dt:.2f} seconds")

    current_file += 1
    show_progress()


# ========================
# SISSIz mono
# ========================
print("\n\nStarted to generate SISSIz mononucleotide samples")
start = time.time()
last_time = start

for z in range(1, ITER + 1):
    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{z}.clu"
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_SISSIz_mono_output_{z}.clu"

    if not os.path.exists(OUTPUT):
        cmd = f"{SISSIZ} -s -i {SISSI_OUTPUT}"
        run_command(cmd, OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"SISSIz_mono sample {z} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nSISSIz_mono runtime: {time.time() - start:.2f} seconds")


# ========================
# SISSIz di
# ========================
print("\nStarted to generate SISSIz dinucleotide samples")
start = time.time()
last_time = start

for v in range(1, ITER + 1):
    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{v}.clu"
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_SISSIZ_di_output_{v}.clu"

    if not os.path.exists(OUTPUT):
        cmd = f"{SISSIZ} -s {SISSI_OUTPUT}"
        run_command(cmd, OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"SISSIz_di sample {v} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nSISSIz_di runtime: {time.time() - start:.2f} seconds")


# ========================
# Multiperm none
# ========================
print("\nStarted to generate Multiperm none samples")
start = time.time()
last_time = start

for m in range(1, ITER + 1):
    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{m}.clu"
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_MULTIPERM_none_output_{m}.clu"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"{MULTIPERM} -w --conservation=none {SISSI_OUTPUT}", shell=True)
        files = glob.glob("perm_001_pos_sample_*.clu")
        if files:
            os.rename(files[0], OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Multiperm_none sample {m} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nMultiperm_none runtime: {time.time() - start:.2f} seconds")


# ========================
# Multiperm level1
# ========================
print("\nStarted to generate Multiperm level1 samples")
start = time.time()
last_time = start

for j in range(1, ITER + 1):
    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{j}.clu"
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_MULTIPERM_level1_output_{j}.clu"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"{MULTIPERM} -w {SISSI_OUTPUT}", shell=True)
        files = glob.glob("perm_001_pos_sample_*.clu")
        if files:
            os.rename(files[0], OUTPUT)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Multiperm_level1 sample {j} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\nMultiperm_level1 runtime: {time.time() - start:.2f} seconds")


# ========================
# Alnshuffle
# ========================
print("\nStarted to generate Alnshuffle samples")
start = time.time()
last_time = start

for k in range(1, ITER + 1):
    SISSI_OUTPUT = f"{SAMPLESCLUSTAL}/pos_sample_output_{k}.clu"
    OUTPUT = f"{SAMPLESCLUSTAL}/neg_sample_ALNSHUFFLE_output_{k}.clu"

    if not os.path.exists(OUTPUT):
        subprocess.run(f"perl {ALNSHUFFLE} < {SISSI_OUTPUT} > {OUTPUT}", shell=True)
        print(f"{OUTPUT} finished")
    else:
        print(f"{OUTPUT} already exists, skipping...")

    last_time, dt = elapsed(start, last_time)
    print(f"Alnshuffle sample {k} took {dt:.2f} seconds")

    current_file += 1
    show_progress()

print(f"\Alnshuffle runtime: {time.time() - start:.2f} seconds")