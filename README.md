# Elalytics Data Processing Respository

Prerequisites:

- Python 3.7

## How to set up the dev environment

1. Clone the repository
2. Open the repository in your IDE (Preferably VSCode). The root directory of the repository should be the root directory of the project in your IDE.
3. Create a virtual environment with `python3 -m venv .venv` while being in the root directory of the repository
4. Activate the virtual environment
   - On Windows: `.venv\Scripts\Activate`
   - On Mac/Linux: `source .venv/bin/activate`
5. Install the dependencies with `pip install -r requirements.txt`
6. Initialize the packages with `pip install -e src`

## Project Structure

├── .venv
│ ├── (children_folders)
├── src
│ ├── (children_folders)
├── .gitignore
├── README.md
└── requirements.txt
