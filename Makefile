PYTHON ?= python

setup:
	$(PYTHON) -m pip install -r requirements.txt
	mkdir -p data/source data/bronze data/silver data/gold data/samples

run-all:
	PYTHONPATH=src $(PYTHON) scripts/01_ingest.py
	PYTHONPATH=src $(PYTHON) scripts/02_transform.py
	PYTHONPATH=src $(PYTHON) scripts/03_train.py
	PYTHONPATH=src $(PYTHON) scripts/05_observe.py
	PYTHONPATH=src $(PYTHON) scripts/06_report.py

serve:
	PYTHONPATH=src $(PYTHON) -m uvicorn scripts.api:app --host 127.0.0.1 --port 8000

report:
	PYTHONPATH=src $(PYTHON) scripts/06_report.py

report-serve: report
	$(PYTHON) -m http.server 8080 --directory reports

test:
	PYTHONPATH=src $(PYTHON) -m pytest -q

clean:
	rm -rf data/bronze data/silver data/gold
