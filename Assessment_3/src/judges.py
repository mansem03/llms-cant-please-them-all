from __future__ import annotations

import time
import json
import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

import requests


@dataclass
class JudgeResult:
    judge_name: str
    score: float
    reason: str


JUDGE_PERSONAS: Dict[str, str] = {
    "strict_academic": (
        "You are a strict university essay judge. Reward relevance, logical structure, clarity, "
        "balanced argument, and precise wording. Penalize vague claims and unsupported statements."
    ),
    "creativity_friendly": (
        "You are an essay judge who values originality, engaging style, memorable phrasing, and "
        "clear personal voice, while still requiring relevance to the topic."
    ),
    "concision_friendly": (
        "You are an essay judge who values concise, direct, readable answers. Penalize unnecessary "
        "length, repetition, and over-complication."
    ),
    "skeptical_logic": (
        "You are a skeptical logic-focused judge. Reward careful reasoning, stated limitations, and "
        "avoidance of overclaiming. Penalize emotional language without evidence."
    ),
}


def _extract_json(text: str) -> Optional[dict]:
    text = str(text).strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.S)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return None

    return None


def _clamp_score(value: float) -> float:
    try:
        value = float(value)
    except Exception:
        return 0.0

    if math.isnan(value):
        return 0.0

    return float(max(0.0, min(9.0, value)))


class BaseJudge:
    def judge(self, topic: str, essay: str) -> List[JudgeResult]:
        raise NotImplementedError


class HeuristicJudge(BaseJudge):
    """No-API baseline judge."""

    def judge(self, topic: str, essay: str) -> List[JudgeResult]:
        words = re.findall(r"[A-Za-z']+", essay.lower())
        unique = len(set(words))
        n = max(1, len(words))

        lexical_diversity = unique / n

        topic_words = {
            w.lower().strip(".,!?;:()[]{}\"'")
            for w in topic.split()
            if len(w) > 4
        }

        relevance = sum(1 for w in topic_words if w in set(words)) / max(1, len(topic_words))

        sentence_count = max(1, essay.count("."))
        has_balance = any(
            x in essay.lower()
            for x in ["however", "on the other side", "even so", "still", "although"]
        )
        has_conclusion = any(
            x in essay.lower()
            for x in ["conclusion", "therefore", "overall", "in summary"]
        )

        length_score = min(1.0, n / 220) * (1.0 if n <= 420 else max(0.5, 420 / n))

        structure = min(1.0, sentence_count / 10)
        structure += 0.15 if has_balance else 0
        structure += 0.10 if has_conclusion else 0
        structure = min(1.0, structure)

        strict = 9 * (0.40 * relevance + 0.35 * structure + 0.25 * length_score)
        creative = 9 * (0.25 * relevance + 0.25 * structure + 0.30 * lexical_diversity + 0.20 * length_score)
        concise = 9 * (0.35 * relevance + 0.35 * structure + 0.30 * (1.0 if 120 <= n <= 260 else 0.55))
        skeptical = 9 * (0.35 * relevance + 0.40 * (1.0 if has_balance else 0.5) + 0.25 * structure)

        scores = {
            "strict_academic": strict,
            "creativity_friendly": creative,
            "concision_friendly": concise,
            "skeptical_logic": skeptical,
        }

        return [
            JudgeResult(
                judge_name=name,
                score=round(_clamp_score(score), 2),
                reason="Heuristic baseline score from relevance, structure, length, and lexical diversity.",
            )
            for name, score in scores.items()
        ]


class GeminiJudge(BaseJudge):
    """Real LLM judge using Google Gemini REST API."""

    def __init__(
        self,
        api_key: str,
        model: str = "gemini-2.5-flash",
        timeout: int = 60,
        min_delay_seconds: float = 1.5,
    ):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.min_delay_seconds = min_delay_seconds
        self._last_call_at = 0.0

    def _hide_secret(self, text: str) -> str:
        text = str(text)
        if self.api_key:
            text = text.replace(self.api_key, "[API_KEY_HIDDEN]")
        return text

    def _respect_rate_limit(self) -> None:
        elapsed = time.time() - self._last_call_at
        wait_time = self.min_delay_seconds - elapsed

        if wait_time > 0:
            time.sleep(wait_time)

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("Missing GEMINI_API_KEY in .env file.")

        self._respect_rate_limit()

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

        generation_config = {
            "temperature": 0.0,
            "maxOutputTokens": 512,
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "score": {"type": "NUMBER"},
                    "reason": {"type": "STRING"},
                },
                "required": ["score", "reason"],
            },
        }

        if "2.5" in self.model:
            generation_config["thinkingConfig"] = {"thinkingBudget": 0}

        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": generation_config,
        }

        params = {"key": self.api_key}

        last_error = None

        for attempt in range(6):
            try:
                response = requests.post(
                    url,
                    params=params,
                    json=payload,
                    timeout=self.timeout,
                )

                self._last_call_at = time.time()

                if response.status_code in [429, 500, 502, 503, 504]:
                    safe_text = self._hide_secret(response.text[:300])
                    last_error = f"{response.status_code}: {safe_text}"

                    wait_time = min(60, 5 * (2 ** attempt))
                    print(f"[Gemini retry] {last_error} | waiting {wait_time}s")
                    time.sleep(wait_time)
                    continue

                response.raise_for_status()
                data = response.json()

                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except Exception as exc:
                    safe_data = self._hide_secret(json.dumps(data)[:500])
                    raise RuntimeError(f"Unexpected Gemini response: {safe_data}") from exc

            except requests.exceptions.RequestException as exc:
                last_error = self._hide_secret(str(exc))
                wait_time = min(60, 5 * (2 ** attempt))
                print(f"[Gemini retry] {last_error} | waiting {wait_time}s")
                time.sleep(wait_time)

        raise RuntimeError(f"Gemini retry failed after 6 attempts: {last_error}")

    def judge(self, topic: str, essay: str) -> List[JudgeResult]:
        results: List[JudgeResult] = []

        for name, persona in JUDGE_PERSONAS.items():
            prompt = f"""
{persona}

Task:
Evaluate the essay for the given topic.

Scoring rule:
Give a score from 0 to 9.
0 = very poor
5 = average
9 = excellent

Return ONLY valid JSON using this exact format:
{{"score": 7, "reason": "short explanation"}}

Topic:
{topic}

Essay:
{essay}
""".strip()

            try:
                raw = self._call_gemini(prompt)
                parsed = _extract_json(raw)

                if not parsed:
                    raise RuntimeError(f"Could not parse JSON from Gemini output: {raw[:200]}")

                score = _clamp_score(float(parsed.get("score", 0)))
                reason = str(parsed.get("reason", "No reason provided.")).strip()

            except Exception as exc:
                score = 0.0
                reason = f"Gemini call failed: {self._hide_secret(str(exc))}"

            results.append(
                JudgeResult(
                    judge_name=name,
                    score=round(score, 2),
                    reason=reason,
                )
            )

        return results


class OllamaJudge(BaseJudge):
    """Real local LLM judge using Ollama.

    Before running:
    ollama pull llama3.1:8b
    """

    def __init__(
        self,
        model: str = "llama3.1:8b",
        host: str = "http://localhost:11434",
        timeout: int = 120,
    ):
        self.model = model
        self.host = host.rstrip("/")
        self.timeout = timeout

    def _call_ollama(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0},
        }

        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()

        return response.json().get("response", "")

    def judge(self, topic: str, essay: str) -> List[JudgeResult]:
        results: List[JudgeResult] = []

        for name, persona in JUDGE_PERSONAS.items():
            prompt = f"""
{persona}

Evaluate the essay for the topic.

Return ONLY valid JSON:
{{"score": 7, "reason": "short explanation"}}

Topic:
{topic}

Essay:
{essay}
""".strip()

            try:
                raw = self._call_ollama(prompt)
                parsed = _extract_json(raw)

                if not parsed:
                    raise RuntimeError(f"Could not parse JSON from Ollama output: {raw[:200]}")

                score = _clamp_score(float(parsed.get("score", 0)))
                reason = str(parsed.get("reason", "No reason provided.")).strip()

            except Exception as exc:
                score = 0.0
                reason = f"Ollama call failed: {exc}"

            results.append(
                JudgeResult(
                    judge_name=name,
                    score=round(score, 2),
                    reason=reason,
                )
            )

        return results


def build_judge(
    provider: str,
    gemini_api_key: str = "",
    gemini_model: str = "gemini-2.5-flash",
    ollama_model: str = "llama3.1:8b",
    ollama_host: str = "http://localhost:11434",
) -> BaseJudge:
    provider = provider.lower().strip()

    if provider == "gemini":
        return GeminiJudge(
            api_key=gemini_api_key,
            model=gemini_model,
        )

    if provider == "ollama":
        return OllamaJudge(
            model=ollama_model,
            host=ollama_host,
        )

    return HeuristicJudge()