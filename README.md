# twin_snakes

Genetic algorithm adversarial attack on the DEFCON-31 "Granny" image classifcation model.

An API Key from https://crucible.dreadnode.io/ is needed 

API key settings located in /src/config.py

GA perturbs an image to maximize the probability of a given target class "Granny Smith"

By default, this code runs using the default timber_wolf image, but is setup to test with any local image

## Installation

```bash
pip install -r requirements.txt

## Setup
```bash
chmod +x setup.sh
./setup.sh

## Running
```bash
twin_snakes [optional_file_path]