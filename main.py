"""
Prompt Engineering Runbook — 5 Production Agents
A toolkit of battle-tested pydantic-ai agents for common engineering tasks.
Each agent uses structured outputs so results are always machine-readable.

Endpoints:
  POST /analyze/swot       — SWOT analysis of any idea or situation
  POST /generate/post      — LinkedIn/Twitter post from rough notes
  POST /review/code        — Code review with actionable feedback
  POST /summarize          — Multi-format document summarizer
  POST /decide             — Decision framework (pros/cons + recommendation)
  GET  /health
"""
import os
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic_ai import Agent
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    raise RuntimeError("Missing ANTHROPIC_API_KEY")


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 1 — SWOT Analyzer
# ═══════════════════════════════════════════════════════════════════════════════
class SWOTResult(BaseModel):
    topic: str
    strengths: list[str]      # 3-5 items
    weaknesses: list[str]     # 3-5 items
    opportunities: list[str]  # 3-5 items
    threats: list[str]        # 3-5 items
    executive_summary: str    # 3-4 sentence synthesis
    top_recommendation: str   # single most important action to take


swot_agent = Agent(
    "anthropic:claude-haiku-4-5",
    result_type=SWOTResult,
    system_prompt=(
        "Perform rigorous SWOT analysis. Be specific and actionable — avoid generic statements. "
        "Strengths/Weaknesses are internal factors. Opportunities/Threats are external. "
        "The executive summary should synthesize all 4 quadrants into a strategic picture. "
        "The top recommendation must be concrete and immediately actionable."
    ),
)


class SWOTRequest(BaseModel):
    topic: str       # the idea, product, company, or decision to analyze
    context: str = ""  # optional background


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 2 — Social Post Generator
# ═══════════════════════════════════════════════════════════════════════════════
class SocialPost(BaseModel):
    platform: str
    post_text: str          # ready-to-publish, includes hashtags
    hook: str               # the opening line (most important for algorithm)
    call_to_action: str     # what the reader should do
    hashtags: list[str]     # 3-8 relevant hashtags
    character_count: int
    tone: str               # professional | casual | inspiring | educational


social_agent = Agent(
    "anthropic:claude-haiku-4-5",
    result_type=SocialPost,
    system_prompt=(
        "Write high-performing social media posts. "
        "For LinkedIn: professional tone, 150-300 words, 3-5 hashtags, end with a question to drive comments. "
        "For Twitter/X: punchy hook under 100 chars, 240 chars max total, 3-5 hashtags, conversational. "
        "The hook must create curiosity or make a bold claim. "
        "Never use generic openers like 'Excited to share...' or 'Thrilled to announce...'. "
        "Write as a thought leader, not a press release."
    ),
)


class SocialRequest(BaseModel):
    notes: str                                         # rough notes or key points
    platform: Literal["linkedin", "twitter", "both"] = "linkedin"
    tone: str = "professional"                         # professional | casual | inspiring


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 3 — Code Reviewer
# ═══════════════════════════════════════════════════════════════════════════════
class CodeIssue(BaseModel):
    line_range: str    # e.g. "12-15" or "42"
    severity: str      # critical | warning | suggestion
    category: str      # security | performance | readability | correctness | style
    issue: str         # what's wrong
    fix: str           # exactly what to change


class CodeReview(BaseModel):
    language: str
    overall_score: int        # 1-10
    summary: str              # 2-3 sentence overall assessment
    issues: list[CodeIssue]   # specific findings
    positive_aspects: list[str]  # what was done well
    refactored_snippet: str   # most important fix shown as code


code_review_agent = Agent(
    "anthropic:claude-sonnet-4-5",   # use sonnet for code — haiku misses subtle bugs
    result_type=CodeReview,
    system_prompt=(
        "You are a senior software engineer doing a thorough code review. "
        "Prioritize: security vulnerabilities (injection, auth bypasses, data exposure), "
        "correctness bugs (off-by-one, null handling, race conditions), "
        "performance issues (N+1 queries, unnecessary re-renders, missing indexes), "
        "then style/readability. "
        "Be specific about what to change — include the exact fix, not just 'improve error handling'. "
        "The refactored_snippet should show the most critical fix as actual code. "
        "Score 9-10 only for production-grade code with no significant issues."
    ),
)


class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
    context: str = ""  # what this code does / PR description


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 4 — Multi-Format Summarizer
# ═══════════════════════════════════════════════════════════════════════════════
class Summary(BaseModel):
    title: str
    one_liner: str         # 1 sentence, max 20 words
    tldr: str              # 2-3 sentences (Twitter thread intro level)
    key_points: list[str]  # 5-7 bullets, each max 20 words
    full_summary: str      # 2-3 paragraphs, structured prose
    action_items: list[str]  # concrete next steps (if any)
    source_type: str       # article | paper | meeting | email | code | other


summarizer_agent = Agent(
    "anthropic:claude-haiku-4-5",
    result_type=Summary,
    system_prompt=(
        "Summarize documents into multiple formats simultaneously. "
        "The one_liner must be understandable without context. "
        "Key points should be the most information-dense takeaways. "
        "Full summary should read like a well-structured briefing, not a bullet list. "
        "Action items only if the source explicitly calls for actions — don't invent them. "
        "Be accurate; do not add information not present in the source."
    ),
)


class SummarizeRequest(BaseModel):
    content: str
    source_type: str = "article"  # article | paper | meeting | email | code


# ═══════════════════════════════════════════════════════════════════════════════
# AGENT 5 — Decision Framework
# ═══════════════════════════════════════════════════════════════════════════════
class DecisionOption(BaseModel):
    option: str
    pros: list[str]      # 3-5 concrete pros
    cons: list[str]      # 3-5 concrete cons
    risk_level: str      # low | medium | high
    effort: str          # low | medium | high
    score: float         # 0-10 composite score


class DecisionResult(BaseModel):
    question: str
    options: list[DecisionOption]
    recommendation: str          # which option and why (2-3 sentences)
    key_tradeoff: str            # the single most important tradeoff to understand
    confidence: str              # high | medium | low
    what_would_change_answer: str  # what new info would flip the recommendation


decision_agent = Agent(
    "anthropic:claude-haiku-4-5",
    result_type=DecisionResult,
    system_prompt=(
        "You are a strategic advisor helping make high-stakes decisions. "
        "Evaluate each option honestly — don't optimize for 'all options look equal'. "
        "The recommendation must be direct: name the winning option and why. "
        "Score options 0-10 based on pros/cons weighted by impact, not count. "
        "The key tradeoff should be the fundamental tension, not a list. "
        "What_would_change_answer forces you to identify hidden assumptions."
    ),
)


class DecisionRequest(BaseModel):
    question: str
    options: list[str]       # 2-4 options to evaluate
    context: str = ""        # constraints, goals, or relevant background
    criteria: list[str] = [] # optional: what matters most (e.g., speed, cost, risk)


# ═══════════════════════════════════════════════════════════════════════════════
# FastAPI app
# ═══════════════════════════════════════════════════════════════════════════════
app = FastAPI(title="Prompt Engineering Runbook", version="1.0.0")


@app.post("/analyze/swot", response_model=SWOTResult)
async def analyze_swot(req: SWOTRequest):
    result = await swot_agent.run(
        f"Topic: {req.topic}\n\nContext: {req.context or 'None provided'}"
    )
    return result.data


@app.post("/generate/post")
async def generate_post(req: SocialRequest):
    if req.platform == "both":
        linkedin_result = await social_agent.run(
            f"Platform: linkedin\nTone: {req.tone}\nNotes:\n{req.notes}"
        )
        twitter_result = await social_agent.run(
            f"Platform: twitter\nTone: {req.tone}\nNotes:\n{req.notes}"
        )
        return {
            "linkedin": linkedin_result.data,
            "twitter": twitter_result.data,
        }

    result = await social_agent.run(
        f"Platform: {req.platform}\nTone: {req.tone}\nNotes:\n{req.notes}"
    )
    return result.data


@app.post("/review/code", response_model=CodeReview)
async def review_code(req: CodeReviewRequest):
    result = await code_review_agent.run(
        f"Language: {req.language}\n"
        f"Context: {req.context or 'None provided'}\n\n"
        f"Code:\n```{req.language}\n{req.code}\n```"
    )
    return result.data


@app.post("/summarize", response_model=Summary)
async def summarize(req: SummarizeRequest):
    result = await summarizer_agent.run(
        f"Source type: {req.source_type}\n\nContent:\n{req.content[:10000]}"
    )
    return result.data


@app.post("/decide", response_model=DecisionResult)
async def decide(req: DecisionRequest):
    options_text = "\n".join(f"- {opt}" for opt in req.options)
    criteria_text = "\n".join(f"- {c}" for c in req.criteria) if req.criteria else "Not specified"
    result = await decision_agent.run(
        f"Question: {req.question}\n\n"
        f"Options:\n{options_text}\n\n"
        f"Context: {req.context or 'None provided'}\n\n"
        f"Key criteria:\n{criteria_text}"
    )
    return result.data


@app.get("/health")
def health():
    return {
        "status": "ok",
        "agents": ["swot", "social-post", "code-review", "summarizer", "decision"],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004, reload=True)
