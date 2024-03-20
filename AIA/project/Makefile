# Detect OS
ifeq ($(OS),Windows_NT)
    # Windows settings
    PYTHON = python
    PIP = pip
    VENV = venv
    SEP = \\
    RM = - rd /s /q
    SCRIPTS = Scripts
else
    # Unix/Linux settings
    PYTHON = python3
    PIP = pip3
    VENV = venv
    SEP = /
    RM = rm -rf
    SCRIPTS = bin
endif

# Main target
all: install

# Create a virtual environment
venv:
	$(PYTHON) -m $(VENV) venv

# Install project dependencies
install: venv
	.$(SEP)venv$(SEP)$(SCRIPTS)$(SEP)$(PIP) install -r requirements.txt

run:
	.$(SEP)venv$(SEP)$(SCRIPTS)$(SEP)$(PYTHON) src$(SEP)__main__.py

executable:
	.$(SEP)venv$(SEP)$(SCRIPTS)$(SEP)pyinstaller src$(SEP)__main__.py --onefile --name cohesion

clean:
	$(RM) venv
	$(RM) src$(SEP)__pycache__