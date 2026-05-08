import os

def loadConfig(path):
    config = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)

                # 🔥 DAS IST DER FIX
                value = os.path.expandvars(value.strip())

                config[key.strip()] = value

    return config