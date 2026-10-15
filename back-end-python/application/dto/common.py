"""Shared helpers for DTO aliases."""
import warnings

warnings.filterwarnings(
    "ignore", message="The 'validation_alias' attribute", category=UserWarning
)

from typing import Annotated, Optional
from pydantic import AliasChoices, Field


def aliases(name: str) -> AliasChoices:
    return AliasChoices(name, name.lower(), name[0].lower() + name[1:] if name else name)
