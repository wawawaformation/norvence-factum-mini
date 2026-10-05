.PHONY: install test fmt lint cov cov-lines cov-summary cov-html

install:
	uv sync

test:
	uv run pytest -v

fmt:
	uv run ruff format .
	uv run ruff check --fix .

lint:
	uv run ruff check .

# --- Couverture de code (brief « Pourquoi la CI était-elle verte ? ») ---

# Q1 : rapport lignes + branches, avec les lignes manquantes
cov:
	uv run pytest --cov=app --cov-branch --cov-report=term-missing

# Q1 : couverture de lignes seule (sans --cov-branch, Cover = % de lignes)
cov-lines:
	uv run pytest --cov=app --cov-report=term-missing

# Q1 : % de lignes et % de branches séparés, fichier par fichier (via coverage.json)
cov-summary:
	uv run pytest -q --cov=app --cov-branch --cov-report=json
	uv run python -c "import json; files = json.load(open('coverage.json'))['files']; print('\n'.join('%-22s lignes %6.2f %%   branches %6.2f %%' % (n, f['summary']['percent_statements_covered'], f['summary']['percent_branches_covered']) for n, f in files.items()))"

# Rapport HTML détaillé (branches partielles en jaune) : ouvrir htmlcov/index.html
cov-html:
	uv run pytest --cov=app --cov-branch --cov-report=html
