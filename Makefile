# Makefile

# Variables
PYLINT = pylint
PYLINTRC = ../.pylintrc
PYLINT_ARGS = $(SOURCE_DIR)/**/*.py --output-format=text --rcfile=pyproject.toml
MYPY =  --config-file pyproject.toml
FLAKE8 = flake8 --config pyproject.toml

# new modules
PYTHON = python3.11
PIP = $(PYTHON) -m pip
SOURCE_DIR = src/commons
TEST_DIR = src/tests
RUFF = ruff --config pyproject.toml

# Phony targets
.PHONY: help install format lint test clean build check

# Default target
help:
	@echo "Available commands:"
	@echo "  make install    : Install dependencies"
	@echo "  make format     : Format code using Black and isort"
	@echo "  make lint       : Run linters"
	@echo "  make test       : Run tests"
	@echo "  make clean      : Remove build artifacts"
	@echo "  make build      : Runs all above to deploy"

# Install dependencies
install:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r requirements-dev.txt
	mypy $(MYPY_ARGS) --install-types --non-interactive $(SOURCE_DIR)

# Format code
format:
	black $(SOURCE_DIR)
	black $(SOURCE_DIR)/$(TEST_DIR)
	isort $(SOURCE_DIR)
	isort $(TEST_DIR)

# Lint code
lint:
	#mypy $(MYPY)  $(SOURCE_DIR)
	$(RUFF) format $(SOURCE_DIR)/**/*.py --target-version py311  -n
	$(RUFF) check $(SOURCE_DIR)/**/*.py
	#$(FLAKE8) $(SOURCE_DIR)/**/*.py
	#$(FLAKE8) $(TEST_DIR)/*.py
	#pylint $(SOURCE_DIR)/**/*.py $(PYLINT_ARGS)
	#pylint $(SOURCE_DIR)/$(TEST_DIR) $(PYLINT_ARGS)

# Run tests
test:
	$(PYTHON) -m pytest $(SOURCE_DIR)/$(TEST_DIR)

# Clean build artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache

# run the phony as bellow
build:
	make clean
	make install
	make format
	make lint
	make test
