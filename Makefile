MODULE=mitrecve


require:
	python3 -m pip install -r requirements.txt

requiretest:
	python3 -m pip install -e .[test]

test:
	python3 -m pytest

coverage:
	python3 -m pytest --cov=./ --cov-report=xml

clean:
	rm -rf __pycache__
	rm -rf */__pycache__
	rm -rf .pytest_cache
	rm -rf coverage.xml .coverage
	rm -rf .vscode

fclean: clean
	rm -rf build/
	rm -rf dist/
	rm -rf ${MODULE}.egg-info

build:
	python3 setup.py sdist bdist_wheel --bdist-dir ~/temp/bdistwheel

deploy:
	twine check dist/*
	twine upload dist/*

.PHONY:  clean fclean test coverage
