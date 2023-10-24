pretty:
	isort etfpy/ && isort tests/
	black etfpy/ && black tests/

run:
	streamlit run app.py
cov:
	coverage run --source=fin_streamlit -m pytest tests/ -vv -ss && coverage report -m
test:
	python tests/ -vv -ss
