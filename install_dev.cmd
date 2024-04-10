echo Install python_template development environment.
call install.cmd
call venv\Scripts\activate
pip install -r requirements-dev.txt
pip install -e .
pre-commit install --install-hooks
deactivate
