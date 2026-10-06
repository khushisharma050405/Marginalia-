from typing import Literal, Optional, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict


class SolveRequest(BaseModel):
    board: Literal["CBSE", "ICSE"] = "CBSE"
    class_level: str = Field(default="10", description="Nursery, LKG, UKG, 1..12")
    stream: Optional[Literal["Science", "Commerce", "Humanities"]] = None  # only 11-12
    subject: str = "General"
    chapter: str = ""
    topics: list[str] = []
    question: str = Field(..., min_length=3, max_length=2000)
    marks: Optional[int] = Field(None, ge=1, le=10)  # optional, drives answer length

    @field_validator("board", mode="before")
    @classmethod
    def normalize_board(cls, v: str) -> str:
        if isinstance(v, str):
            v_up = v.strip().upper()
            if v_up in ("CBSE", "ICSE"):
                return v_up
        return "CBSE"

    @field_validator("question")
    @classmethod
    def strip_question(cls, v: str) -> str:
        return v.strip()


class RelevanceResult(BaseModel):
    relevant: bool
    scope: Literal["in_chapter", "other_chapter_same_subject", "other_subject", "not_academic"]
    suggested_chapter: Optional[str] = None
    reason: str


class DiagramInfo(BaseModel):
    type: Literal["graph", "flowchart", "svg_library", "svg_generated", "none"] = "none"
    title: Optional[str] = None
    data: Optional[Any] = None  # For graph: dict, flowchart: str (mermaid), svg_library/svg_generated: str (svg or key)
    library_key: Optional[str] = None
    note: Optional[str] = None  # E.g. "AI-drawn. Verify with your textbook."

    model_config = ConfigDict(extra="allow")


class SolveResponse(BaseModel):
    topic_matched: str = "General"
    definition: Optional[str] = None          # short, only if the question asks for one
    explanation: list[str] = []               # points/steps, at most marks count
    formula: Optional[str] = None
    working: list[str] = []                   # numerical steps, with units
    final_answer: str = ""
    confidence: Literal["high", "medium", "low"] = "high"
    used_context: bool = False                # True if answer came from retrieved chapter text
    diagram: Optional[DiagramInfo] = None

    # Compatibility fields for frontend rendering & notes saving
    solved: bool = True
    subject: Optional[str] = None
    topic: Optional[str] = None
    steps: list[tuple[str, str]] = []
    direct_answer: Optional[str] = None
    verification_badge: Optional[str] = None
    extracted: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    @field_validator("explanation", "working", "steps", mode="before")
    @classmethod
    def ensure_list(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]


class SelfCheckResult(BaseModel):
    factually_correct: bool = True
    in_scope_for_class: bool = True      # not too advanced, not too basic
    complete: bool = True                # nothing important missing
    issues: list[str] = []
    corrected: Optional[SolveResponse] = None

    model_config = ConfigDict(extra="allow")

    @field_validator("issues", mode="before")
    @classmethod
    def ensure_issues_list(cls, v):
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return [v]
