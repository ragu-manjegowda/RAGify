.PHONY: activate install run clean deactivate

activate:
	python -m venv .venv
	source .venv/bin/activate

install:
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm -rf __pycache__ .vector_store

deactivate:
	deactivate
