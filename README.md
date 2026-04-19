# Pronóstico del tiempo, Facultad de Ciencias Astronómicas y Geofísicas - UNLP

API for the Pronostico UNLP website.

Based on their former [web page](https://www.fcaglp.unlp.edu.ar/index.php/pronostico-del-tiempo/)

## Run the app

The following instructions are for a Linux system.

After cloning the project we need to follow these steps:

1. Create and activate a python virtual environment
2. Install the project dependencies
3. Finally run the app

### 1. Creating a virtual environment

Steps to create a python virtual env:

- Create the `.venv` file in your project directory:

```bash
python3 -m venv .venv
```

`-m` : It stands for "module" and is used to specify that you want to run a Python module as a script.
`venv`: is a package in the Python Standard Library for creating lightweight Virtual Environments.
Read more on [venv official python doc](https://docs.python.org/3/library/venv.html).

- Activate virtual env:

```bash
source .venv/bin/activate
```

### 2. Installing dependencies

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Run the flask application

```bash
flask run
```

*Deactivate venv* when finish.
You can deactivate a virtual environment by typing `deactivate` in your shell.

## Testing db scripts

```bash
# Activate virtual environment
. .venv/bin/activate

# Clean existing data (optional)
python3 scripts/seed_data.py clear

# Create all data with the new structure
python3 scripts/seed_data.py create

# Verify the created data
python3 scripts/seed_data.py list
```

