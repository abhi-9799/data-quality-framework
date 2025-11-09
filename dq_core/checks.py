from dataclasses import dataclass
from sqlalchemy import text
from datetime import datetime, timezone

@dataclass
class CheckResult:
    passed: bool
    message: str
    failed_rows: int = 0

def nulls_check(engine, table: str, column: str, max_null_pct: float = 0.0) -> CheckResult:
    with engine.connect() as conn:
        total = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar_one()
        nulls = conn.execute(text(f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL")).scalar_one()
    pct = (nulls / total) * 100 if total else 0.0
    passed = pct <= (max_null_pct * 100)
    msg = f"Nulls {pct:.2f}% (limit {(max_null_pct*100):.2f}%)"
    return CheckResult(passed=passed, message=msg, failed_rows=nulls)

def uniqueness_check(engine, table: str, column: str, max_dupes: int = 0):
    """
    Fails if any value appears more than once in `column`.
    Returns number of duplicate values (not rows).
    """
    from sqlalchemy import text
    with engine.connect() as conn:
        sql = f"""
          SELECT COUNT(*) FROM (
            SELECT {column}
            FROM {table}
            GROUP BY {column}
            HAVING COUNT(*) > 1
          ) t;
        """
        dup_values = conn.execute(text(sql)).scalar_one()
    passed = dup_values <= max_dupes
    msg = f"Duplicate values: {dup_values} (allowed <= {max_dupes})"
    return CheckResult(passed=passed, message=msg, failed_rows=int(dup_values))

def referential_check(engine,
                      source_table: str, source_column: str,
                      target_table: str, target_column: str,
                      max_violations: int = 0) -> CheckResult:
    """
    Count rows in source where the FK value has no match in target.
    """
    from sqlalchemy import text
    with engine.connect() as conn:
        sql = f"""
          SELECT COUNT(*) FROM {source_table} s
          LEFT JOIN {target_table} t
            ON s.{source_column} = t.{target_column}
          WHERE t.{target_column} IS NULL;
        """
        violations = conn.execute(text(sql)).scalar_one()
    passed = violations <= max_violations
    msg = f"RI violations: {violations} (allowed <= {max_violations})"
    return CheckResult(passed=passed, message=msg, failed_rows=int(violations))

def freshness_check(engine, table: str, ts_col: str, max_age_hours: float) -> CheckResult:
    """
    Assumes ISO8601 timestamps in UTC (e.g., 2025-11-08T10:00:00).
    Fails if (now - max(ts_col)) > max_age_hours.
    """
    from sqlalchemy import text
    with engine.connect() as conn:
        max_ts_text = conn.execute(text(f"SELECT MAX({ts_col}) FROM {table}")).scalar_one()
    if max_ts_text is None:
        return CheckResult(passed=False, message="No timestamps present", failed_rows=0)

    try:
        # Treat naive timestamps as UTC
        max_ts = datetime.fromisoformat(str(max_ts_text))
        if max_ts.tzinfo is None:
            max_ts = max_ts.replace(tzinfo=timezone.utc)
    except Exception:
        return CheckResult(passed=False, message=f"Unparseable timestamp: {max_ts_text}", failed_rows=0)

    now = datetime.now(timezone.utc)
    age_hours = (now - max_ts).total_seconds() / 3600.0
    passed = age_hours <= max_age_hours
    msg = f"Age={age_hours:.2f}h (limit {max_age_hours}h)"
    return CheckResult(passed=passed, message=msg)
