lint:
	python3 gamedi/manage.py check
	flake8 .
	mypy .
