"""配置管理"""

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    api_key: str = field(default_factory=lambda: os.getenv("VULSENSE_API_KEY", ""))
    llm_model: str = "deepseek-chat"
    llm_endpoint: str = "https://api.deepseek.com"
    output_dir: str = "."

    @classmethod
    def from_env(cls) -> "Config":
        return cls()

    @property
    def has_llm(self) -> bool:
        return bool(self.api_key)
