lint:
	python3 gamedi/manage.py check
	flake8 .
	mypy .

test:
	pytest --cov=gamedi gamedi/pytest_tests
