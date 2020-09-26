virtualenv:
	python -m venv venv
install:
	pip install -r requirements.txt
migrate:
	FLASK_SKIP_DOTENV=1 flask db upgrade head
rollback:
	FLASK_SKIP_DOTENV=1 flask db  downgrade -1
clean:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
