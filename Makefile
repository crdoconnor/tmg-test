.PHONY: build
build:
	rm -rf ./venv
	virtualenv venv
	./venv/bin/pip install -r requirements.txt

.PHONY: run
run: ## Run application locally
	./venv/bin/uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8080

.PHONY: test
test: ## Run tests
	./venv/bin/pytest -s test_recipes.py
