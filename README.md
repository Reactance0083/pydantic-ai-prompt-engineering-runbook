# Prompt Engineering Runbook — 5 Production Agents (pydantic-ai + FastAPI)

A toolkit of 5 battle-tested pydantic-ai agents for common engineering and business tasks. Every response is structured (typed Pydantic models) so outputs are always machine-readable and composable.

## The 5 Agents

| Endpoint | Agent | Model | Use Case |
|----------|-------|-------|---------|
| `POST /analyze/swot` | SWOT Analyzer | haiku | Strategic analysis of any idea, product, or company |
| `POST /generate/post` | Social Post Generator | haiku | LinkedIn/Twitter posts from rough notes |
| `POST /review/code` | Code Reviewer | **sonnet** | Code review with specific line-level feedback |
| `POST /summarize` | Multi-Format Summarizer | haiku | Articles, papers, meeting notes → structured summaries |
| `POST /decide` | Decision Framework | haiku | Pros/cons matrix with a clear recommendation |

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in ANTHROPIC_API_KEY
uvicorn main:app --reload --port 8004
```

Interactive docs at: http://localhost:8004/docs

## API Examples

### SWOT Analysis

```bash
curl -X POST http://localhost:8004/analyze/swot \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Launching a pydantic-ai template marketplace on Gumroad",
    "context": "Solo developer, $0 marketing budget, existing crypto Twitter audience"
  }'
```

Returns: `strengths`, `weaknesses`, `opportunities`, `threats`, `executive_summary`, `top_recommendation`

### Social Post Generator

```bash
curl -X POST http://localhost:8004/generate/post \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Just shipped 5 production pydantic-ai templates. They include Slack→Notion, GitHub triage, cost optimizer, web scraper, and a prompt runbook. Sharing on GitHub.",
    "platform": "both",
    "tone": "professional"
  }'
```

Returns: LinkedIn and Twitter posts with hook, hashtags, and CTA.

### Code Review

```bash
curl -X POST http://localhost:8004/review/code \
  -H "Content-Type: application/json" \
  -d '{
    "code": "async def get_user(id): return db.query(f\"SELECT * FROM users WHERE id={id}\")",
    "language": "python",
    "context": "User lookup endpoint in FastAPI"
  }'
```

Returns: `overall_score`, `issues` (with line ranges and fixes), `positive_aspects`, `refactored_snippet`.

### Summarizer

```bash
curl -X POST http://localhost:8004/summarize \
  -H "Content-Type: application/json" \
  -d '{
    "content": "...(paste article text)...",
    "source_type": "article"
  }'
```

Returns: `one_liner`, `tldr`, `key_points`, `full_summary`, `action_items`.

### Decision Framework

```bash
curl -X POST http://localhost:8004/decide \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Should I use Supabase or PlanetScale for the new SaaS?",
    "options": ["Supabase", "PlanetScale", "Self-hosted Postgres"],
    "context": "Solo dev, need auth + DB, $50/mo budget, scaling to 10k users",
    "criteria": ["cost", "developer experience", "scalability"]
  }'
```

Returns: scored options with pros/cons, recommendation, key tradeoff, and what would change the answer.

## Structured Output Examples

### Code Review Output

```python
class CodeReview(BaseModel):
    language: str
    overall_score: int        # 1-10
    summary: str
    issues: list[CodeIssue]   # [{line_range, severity, category, issue, fix}]
    positive_aspects: list[str]
    refactored_snippet: str
```

### Decision Output

```python
class DecisionResult(BaseModel):
    question: str
    options: list[DecisionOption]  # [{option, pros, cons, risk_level, effort, score}]
    recommendation: str
    key_tradeoff: str
    confidence: str
    what_would_change_answer: str
```

## Model Choice

The code reviewer uses `claude-sonnet-4-5` because haiku misses subtle security bugs and logic errors. All other agents use `claude-haiku-4-5` — the tasks are structured enough that haiku performs at sonnet-level quality at 10x lower cost.

## Composability

These agents are designed to chain. Example: run SWOT → pipe `top_recommendation` into Decision Framework → pipe winning option into Social Post Generator to announce it.

## Requirements

- Python 3.11+
- Anthropic API key (haiku for 4 agents, sonnet for code review)
- Estimated cost: ~$0.005 per 10 requests (mostly haiku)

---

## Get the Complete Bundle

All 5 templates are available individually or as a **$39 bundle** (saves $15 vs individual).

| Template | Price | Link |
|----------|-------|------|
| Slack → Notion Automation | $9 | [Buy on Gumroad](https://reactance0083.gumroad.com/l/cdonwt) |
| GitHub Issue → Linear Triage | $9 | [Buy on Gumroad](https://reactance0083.gumroad.com/l/axgwj) |
| Multi-LLM Cost Optimizer | $12 | [Buy on Gumroad](https://reactance0083.gumroad.com/l/ztmlv) |
| Web Scraper + Semantic Search | $9 | [Buy on Gumroad](https://reactance0083.gumroad.com/l/esjukw) |
| Prompt Engineering Runbook | $15 | [Buy on Gumroad](https://reactance0083.gumroad.com/l/mdsbpc) |
| **Complete Bundle (all 5)** | **$39** | [Buy on Gumroad](https://reactance0083.gumroad.com/l/pydantic-ai-fastapi-bundle) |

Buying includes: all source files, README, requirements.txt, .env.example, and lifetime updates.

> **Free to use** — the source is here on GitHub. Buying supports continued development and gets you a clean download with everything packaged.

---

*Built by [Wade Allen](https://github.com/Reactance0083) — AI Workflow Architect*
