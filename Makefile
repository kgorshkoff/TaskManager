test:
	coverage run -m pytest tests/
	coveralls

black:
	black .
