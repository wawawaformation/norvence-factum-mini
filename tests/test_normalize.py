import json
from decimal import Decimal
from pathlib import Path

import pytest

from app.normalize import normalize_amount

# Échantillons réels de factures : un objet JSON par ligne (format JSONL)
SAMPLES_FILE = Path(__file__).parent / "fixtures" / "echantillons.jsonl"
SAMPLES = [json.loads(line) for line in SAMPLES_FILE.read_text(encoding="utf-8").splitlines()]


# Un test par échantillon, nommé par l'identifiant de la facture (F-0137…)
@pytest.mark.parametrize("sample", SAMPLES, ids=[sample["id"] for sample in SAMPLES])
def test_normalize_samples(sample):
    # montant_attendu est une chaîne : on la convertit en Decimal pour comparer des valeurs
    assert normalize_amount(sample["montant_brut"]) == Decimal(sample["montant_attendu"])


# Entier ou flottant : arrondi au centime sans passer par le parsing du texte
@pytest.mark.parametrize("raw, expected", [(1250, "1250.00"), (980.5, "980.50")])
def test_normalize_numeric_input(raw, expected):
    assert normalize_amount(raw) == Decimal(expected)


def test_normalize_missing_amount():
    # Un montant absent doit être refusé, pas converti en 0
    with pytest.raises(ValueError):
        normalize_amount(None)
