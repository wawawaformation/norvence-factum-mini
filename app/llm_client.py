"""Clients LLM utilisés pour l'extraction des champs de facture."""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Protocol


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str:
        """Renvoie la réponse brute du modèle (une chaîne JSON attendue)."""
        ...


class MockLLMClient:
    """Client déterministe : renvoie une réponse préenregistrée, sans appel réseau."""

    def __init__(self, response: dict | str) -> None:
        self._response = response if isinstance(response, str) else json.dumps(response)
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self._response


class HttpLLMClient:
    """Client réel : appelle le fournisseur LLM configuré via LLM_ENDPOINT / LLM_API_KEY."""

    def __init__(self, endpoint: str | None = None, api_key: str | None = None) -> None:
        self.endpoint = endpoint or os.environ["LLM_ENDPOINT"]
        self.api_key = api_key or os.environ["LLM_API_KEY"]

    def complete(self, prompt: str) -> str:  # pragma: no cover - appel réseau réel, testé hors CI
        body = json.dumps({"prompt": prompt, "temperature": 0}).encode("utf-8")
        request = urllib.request.Request(
            self.endpoint,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload["output"]
