# Structured AI Workflow Runbook

Five PydanticAI workflow references exposed through FastAPI, with typed outputs for common business and engineering tasks.

**[Portfolio](https://github.com/Reactance0083)** · **Status: experimental implementation**

| Endpoint | Output |
| --- | --- |
| `POST /analyze/swot` | Strengths, weaknesses, opportunities, threats, and a recommendation. |
| `POST /generate/post` | Draft social post, tone, hook, and hashtags. |
| `POST /review/code` | Structured issues, severity, suggested fixes, and a review summary. |
| `POST /summarize` | Multiple summary lengths, key points, and action items. |
| `POST /decide` | Options, tradeoffs, recommendation, and uncertainty. |
| `GET /health` | Health and agent names. |

## What the project demonstrates

Task-specific prompts and typed schemas make AI output easier to consume in another workflow. Schema validation establishes structure; it does not establish that every factual claim, score, code fix, or recommendation is correct.

The social route generates text. It does not publish to a social account.

## Local setup

```bash
python -m venv .venv
# Activate the environment for your shell.
python -m pip install -r requirements.txt
# Copy .env.example to .env and set ANTHROPIC_API_KEY.
python -m uvicorn main:app --host 127.0.0.1 --port 8004
```

The application is in `main.py`. Inspect its request models in the local API documentation at `/docs`.

## Limits

No independent evaluation establishes production accuracy or reliability. Review current model availability and PydanticAI compatibility, input limits, authentication, rate limiting, and data handling before deployment. The source uses `result_type` and `result.data`.

Model-generated confidence and scores are not independent measurements. Review outputs before consequential use.

Developed with AI assistance. Documentation reviewed against source on November 10, 2026.
