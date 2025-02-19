.PHONY: activate install run clean deactivate

activate:
	python -m venv .venv
	@echo "Run 'source .venv/bin/activate' to activate the virtual environment"

install:
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm -rf __pycache__ .vector_store

deactivate:
	@echo "Run 'deactivate' to deactivate the virtual environment"
