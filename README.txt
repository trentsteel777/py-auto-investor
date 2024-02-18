To install:
    python -m venv venv
    .\venv\Scripts\activate
    Update requirements.txt to point to TA-Lib in your machine
        You need the correct wheel for your version of Python: https://github.com/cgohlke/talib-build/releases
    python -m pip install -r requirements.txt

To run:
    .\venv\Scripts\activate (make sure virtual enviorment is activated)
    python main.py

Note:
    to deactivate virtual enviorment run in command line: deactivate