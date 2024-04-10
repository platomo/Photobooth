echo Install photobooth.
@echo off
FOR /F "tokens=* USEBACKQ" %%F IN (`python3.11 --version`) DO SET PYTHON_VERSION=%%F

echo %PYTHON_VERSION%
if "x%PYTHON_VERSION:3.11=%"=="x%PYTHON_VERSION%" (
    echo "Python Version 3.11 is not installed in environment." & cmd /K & exit
)

python3.11 -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
deactivate
