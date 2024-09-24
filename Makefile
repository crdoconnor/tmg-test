.PHONY: build
build:
	docker build . -t tmgtestcolm

.PHONY: run
run: ## Run application locally
	docker run -p 8080:8080 tmgtestcolm

.PHONY: test
test: ## Run tests
	docker run --entrypoint pytest -it tmgtestcolm pytest -s test_recipes.py
