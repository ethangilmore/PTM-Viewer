# PTM Viewer

PTM-Viewer is a small GUI program built to quickly analyze and extract peptides with post translational modifications (PTMs) from files generated with [MSFragger](https://github.com/Nesvilab/MSFragger) and [FragPipe](https://github.com/Nesvilab/FragPipe).

# Installation

There are two ways to install and run this software

- For convenience, an executable can be downloaded [here](https://github.com/ethangilmore/PTM-Viewer/releases)

- A manual installation of the source code can be done with the following steps
  1)  Download the source code
  2)  (Optional) Create a python virtual environment
      ```sh
      python -m venv .venv
      ```
      And then activate it (you will have to this whenever you want to run the source code)
      - Windows
          ```sh
          source .venv/Scripts/activate
          ```
      - Mac/Linux
          ```sh
          source .venv/bin/activate
          ```
  3)  Install requirements
      ```sh
      pip install -r requirements.txt
      ```
  4)  Run `main.py` located in the src directory
      ```sh
      python src/main.py
      ```

Manual installation is preferred as it may be much quicker to start up and run.

