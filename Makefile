.PHONY: help install lint format type-check test audit docker-build docker-run train-eeg2emg clean

PYTHON      := python3
IMAGE_NAME  := umbra
IMAGE_TAG   := latest
PORT        := 8501

help:
	@echo "Umbra — available targets:"
	@echo "  install       Install runtime + dev dependencies"
	@echo "  lint          Run ruff linter"
	@echo "  format        Run ruff formatter (in-place)"
	@echo "  type-check    Run mypy type checker"
	@echo "  test          Run pytest with coverage"
	@echo "  audit         Run pip-audit security check"
	@echo "  docker-build  Build the Docker image"
	@echo "  docker-run    Run the Streamlit dashboard in Docker"
	@echo "  train-eeg2emg Train EEG→EMG on dataset_subject_1.npz"
	@echo "  clean         Remove build/cache artifacts"

install:
	pip3 install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	ruff check src/ tests/

format:
	ruff format src/ tests/

type-check:
	mypy src/

test:
	pytest

audit:
	pip-audit -r requirements.txt --format=columns

docker-build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

docker-run:
	docker run --rm -p $(PORT):8501 \
		-v "$(PWD)/data:/app/data:ro" \
		-v "$(PWD)/src/eeg_emg:/app/src/eeg_emg:ro" \
		$(IMAGE_NAME):$(IMAGE_TAG)

train-eeg2emg:
	$(PYTHON) -m src.eeg_emg.eeg2emg_run \
		--data_path data/eeg_emg/dataset_subject_1.npz \
		--normalize \
		--save_path src/eeg_emg/eeg2emg_best.pth

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	rm -f coverage.xml .coverage
