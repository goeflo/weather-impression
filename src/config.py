import yaml

with open("settings.yaml", "r") as f:
    print("reading settings.yaml ...")
    settings = yaml.safe_load(f)
    