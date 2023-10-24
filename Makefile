pretty:
	isort fin_streamlit/ && isort tests/
	black fin_streamlit/ && black tests/

run:
	streamlit run app.py
cov:
	coverage run --source=fin_streamlit -m pytest tests/ -vv -ss && coverage report -m
test:
	python tests/ -vv -ss
