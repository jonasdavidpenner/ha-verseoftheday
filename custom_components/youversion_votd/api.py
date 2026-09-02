"""Schlanker asynchroner Client für die YouVersion Platform API."""

from __future__ import annotations

import logging

from aiohttp import ClientError, ClientSession

from .const import API_BASE, APP_KEY_HEADER

_LOGGER = logging.getLogger(__name__)


class YouVersionError(Exception):
    """Allgemeiner API-Fehler."""


class YouVersionAuthError(YouVersionError):
    """Wird ausgelöst, wenn der App Key ungültig ist oder abgelehnt wird."""


class YouVersionClient:
    """Kapselt die HTTP-Aufrufe gegen die YouVersion Platform API."""

    def __init__(self, session: ClientSession, app_key: str, bible_id: int) -> None:
        self._session = session
        self._app_key = app_key
        self._bible_id = bible_id

    @property
    def _headers(self) -> dict[str, str]:
        return {APP_KEY_HEADER: self._app_key}

    async def _get(self, path: str, params: dict | None = None) -> dict:
        url = f"{API_BASE}{path}"
        try:
            async with self._session.get(
                url, headers=self._headers, params=params
            ) as resp:
                if resp.status in (401, 403):
                    raise YouVersionAuthError(
                        f"App Key abgelehnt (HTTP {resp.status})"
                    )
                resp.raise_for_status()
                return await resp.json()
        except YouVersionAuthError:
            raise
        except ClientError as err:
            raise YouVersionError(f"Verbindungsfehler: {err}") from err

    async def async_list_bibles(self, language: str) -> list[dict]:
        """Listet die für diesen App Key lizenzierten Bibeln einer Sprache auf."""
        data = await self._get(
            "/bibles",
            params={"language_ranges[]": language, "page_size": 99},
        )
        return [
            {
                "id": item["id"],
                "title": item.get("localized_title") or item.get("title") or str(item["id"]),
            }
            for item in data.get("data", [])
        ]

    async def async_get_passage(self, passage_id: str) -> dict:
        """Holt den Text einer Passage in der konfigurierten Übersetzung."""
        return await self._get(
            f"/bibles/{self._bible_id}/passages/{passage_id}",
            params={"format": "text"},
        )

    async def async_get_verse_of_the_day(self, day_of_year: int) -> dict:
        """Holt Referenz + Text für den Vers des Tages."""
        votd = await self._get(f"/verse_of_the_days/{day_of_year}")
        passage_id = votd["passage_id"]
        passage = await self.async_get_passage(passage_id)
        return {
            "passage_id": passage_id,
            "reference": passage.get("reference"),
            "content": passage.get("content"),
        }

    async def async_validate(self) -> None:
        """Prüft App Key und Zugriff auf die gewählte Übersetzung."""
        # JHN.3.16 existiert in jeder Bibel und ist damit ein sicherer Testabruf.
        await self.async_get_passage("JHN.3.16")
