.PHONY: bootstrap demo test verify lint

bootstrap:
	python -m pip install -e ".[dev]"

demo:
	python -m omphalos run --config config/runs/example_run.yaml

test:
	pytest -q

verify:
	python -m omphalos verify --run-dir $$(ls -dt artifacts/runs/* | head -n 1)

lint:
	ruff check .
	mypy src
