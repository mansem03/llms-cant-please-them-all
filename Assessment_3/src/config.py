from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class Config:
    data_dir: Path = Path("data")
    output_dir: Path = Path("outputs")
    judge_provider: str = "heuristic"  # heuristic, gemini, ollama
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    ollama_model: str = "llama3.1:8b"
    ollama_host: str = "http://localhost:11434"
    n_candidates: int = 6
    max_topics: int = 0  # 0 = all topics
    random_seed: int = 42
    use_llm_generator: bool = False

    @classmethod
    def from_env(cls) -> "Config":
        load_dotenv()
        return cls(
            data_dir=Path(os.getenv("DATA_DIR", "data")),
            output_dir=Path(os.getenv("OUTPUT_DIR", "outputs")),
            judge_provider=os.getenv("JUDGE_PROVIDER", "heuristic").lower().strip(),
            gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
            gemini_model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip(),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1:8b").strip(),
            ollama_host=os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/"),
            n_candidates=int(os.getenv("N_CANDIDATES", "6")),
            max_topics=int(os.getenv("MAX_TOPICS", "0")),
            random_seed=int(os.getenv("RANDOM_SEED", "42")),
            use_llm_generator=os.getenv("USE_LLM_GENERATOR", "false").lower() in {"1", "true", "yes"},
        )

    def validate(self) -> None:
        if self.judge_provider not in {"heuristic", "gemini", "ollama"}:
            raise ValueError("JUDGE_PROVIDER must be one of: heuristic, gemini, ollama")
        if self.judge_provider == "gemini" and not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required when JUDGE_PROVIDER=gemini")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
