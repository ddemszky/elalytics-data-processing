# Elalytics Data Processing Respository

## Prerequisites:

- Python 3.11

## How to set up the dev virtual environment for the first time

1. Clone the repository
2. Open the repository in your IDE (Preferably VSCode). The root directory of the repository should be the root directory of the project in your IDE.
3. Create a virtual environment with `python3 -m venv .venv` while being in the root directory of the repository
4. Activate the virtual environment
   - On Windows: `.venv\Scripts\Activate`
   - On Mac/Linux: `source .venv/bin/activate`
5. Install the dependencies with `pip install -r requirements.txt`
6. Initialize the packages with `pip install -e src`
7. Check if everything works by running the notebook in the `src/texts/example` folder
   - VS code might ask you to install several extensions if you are using for the first time. Please do so.
   - You will have to change the kernel of the notebook to the virtual environment. You can do this by clicking on the kernel name in the top right corner of the notebook and selecting the virtual environment.

## Project Structure after the setup

```
├── .venv
│ ├── (children_folders)
├── src
│ ├── (children_folders)
├── .gitignore
├── README.md
└── requirements.txt
```

## How to reactivate the virtual environment

It is important to work within the virtual environment to avoid the clash between different packages. If you close your IDE, you will have to reactivate the virtual environment. You can easily do this by running the following command in the root directory of the repository in your terminal of the IDE:

- On Windows: `.venv\Scripts\Activate`
- On Mac/Linux: `source .venv/bin/activate`

## Important Note

- **Always update the requirements.txt file after installing a new package with the correct version number**
- Always work within the virtual environment
