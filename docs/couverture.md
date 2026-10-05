# Couverture de code

La CI ne lançait que `pytest`, sans mesure de couverture ni seuil : elle ne pouvait devenir rouge que si un test existant échouait.
Or aucun test n'envoyait de montant avec virgule (« 1250.00 », un entier sans `assert`, « 980.50 ») : la branche « virgule » de `normalize_amount` n'était jamais exécutée, et la ligne de son `elif` comptait pourtant comme couverte.
Le correctif ayant été poussé sans test, rien n'a vérifié le cas « 1 250,00 € » ni avant, ni pendant, ni après l'incident : une CI verte signifiait « aucun test existant n'échoue », pas « les montants sont corrects ».

## Seuil retenu

`fail_under = 93` dans `pyproject.toml` (section `[tool.coverage.report]`). La couverture de branches est activée sur `app` dans `[tool.coverage.run]`.

| Mesure (2026-10-05) | Valeur |
| --- | --- |
| Total `app/` (lignes + branches), comparé à `fail_under` | 95,35 % |
| `normalize.py`, branches | 100 % (16/16) |
| État pendant l'incident | 79 %, sans seuil |

Justification :

- 93 est bien au-dessus de l'état qui a laissé passer l'incident : on ne peut plus y revenir sans que la CI devienne rouge.
- Il laisse environ 2 points de marge, pour qu'un refactoring ou une petite fonction pas encore testée ne bloque pas toute l'équipe.
- C'est un **cliquet** : on remonte le seuil quand la couverture progresse, on ne le baisse jamais.
- Le seuil est dans `pyproject.toml` et non dans le workflow : la commande locale et la CI appliquent la même règle.

Ce seuil n'est pas une preuve de qualité. Il empêche la couverture de reculer, mais seuls les `assert` des tests vérifient les valeurs (voir le test paramétré sur `tests/fixtures/echantillons.jsonl`).

## Exclusions

- `HttpLLMClient.complete` (`app/llm_client.py`) est exclue avec `# pragma: no cover` : elle fait un vrai appel réseau au fournisseur LLM (secrets, coût, réponse non déterministe). Les tests utilisent `MockLLMClient` à la place.

## Relancer la mesure en local

```bash
make cov            # rapport lignes + branches avec les lignes manquantes
make cov-summary    # % de lignes et % de branches séparés, par fichier
make cov-html       # rapport détaillé dans htmlcov/index.html
```

Sans `make` :

```bash
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```
