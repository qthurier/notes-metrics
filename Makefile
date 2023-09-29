include *.mk

# add additional targets here

lambda:
	cd notes_metrics; ../$(venv)/bin/chalice --debug deploy --stage prod --profile notes-metrics

local-lambda:
	cd notes_metrics; ../$(venv)/bin/chalice local --autoreload --stage local

clean-lambda:
	$(venv)/bin/chalice --project-dir notes_metrics delete 


