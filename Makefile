test:
	coverage run -m pytest
	coverage report

black:
	black .
