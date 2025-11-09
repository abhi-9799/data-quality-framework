# Data Quality Testing Framework

A small but realistic data-quality validation framework built **step-by-step** using Python + Pytest.  
This project started as a single null check on a CSV → SQLite table and gradually evolved into a reusable mini framework with YAML-driven rules and HTML reporting.

Rather than building everything upfront, the project grew intentionally — one layer at a time — similar to how real QA/data teams improve systems incrementally.

---

## Why I Built This

Most data-quality solutions online either:
- Feel too enterprise/abstract, or  
- Are academic with no connection to real workflows, or  
- Use AI buzzwords without solving fundamentals  

So I built something intentionally grounded:
- Practical
- Understandable
- Reusable
- Tech-stack friendly  

The goal was to show **test discipline + incremental delivery** rather than flashy tooling.

---

## What It Does

Validates tabular data inside SQLite with multiple DQ checks:

| Check Type      | Description |
|-----------------|-------------|
| Nulls           | Column cannot exceed null% threshold |
| Uniqueness      | Key columns must be unique |
| Referential     | Foreign keys must exist in reference tables |
| Freshness       | Data must be up-to-date within time threshold |

All results are summarized in an **HTML report** generated via `pytest-html`.

---

## How It Evolved (Human, Step-by-Step)

1) Loaded example CSV → SQLite  
2) Wrote first test (null check on `amount`)  
3) Added uniqueness check (`order_id`)  
4) Added referential check (orders → customers)  
5) Added freshness check (`ingest_ts`)  
6) Moved validation rules to YAML → config-driven  
7) Added HTML reporting for usability  

> This mirrors how I’d approach real technical growth:  
**Start small → build intuition → expand intentionally.**

---

## Tech Stack

- Python
- Pytest
- SQLAlchemy
- SQLite
- YAML
- pytest-html

---

