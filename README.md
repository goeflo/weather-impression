# weather-impression

Display weather information on an Inky Impression 7.3" (7 colour ePaper) from pimorini.

![weather display](https://github.com/goeflo/weather-impression/blob/main/display.jpg)


## howto setup

### create a python virtual environment

```
python -m venv .venv
```

### activate python virtual environment

```
source .venv/bin/activate
```

### install dependencies

```
python3 -m pip install -r requirements.txt
```

### install open meteo python library

```
pip install git+https://github.com/m0rp43us/openmeteopy
```

### edit configuration file

```
vim src/settings.yaml
```

### run display

```
./main.py
```

### test and development

For testing it is possible to get only one update on the weather information and
the generated image is stored on the filesystem:

```
./main.py -e
```

# links

[Open Meteo](https://open-meteo.com)

[inky python library](https://github.com/pimoroni/inky)

[open meteo python library](https://github.com/m0rp43us/openmeteopy/tree/main)

