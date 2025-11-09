import os
from dq_core.load_seed import load_sqlite
from dq_core.spec_loader import load_specs
from dq_core.checks import nulls_check, uniqueness_check, referential_check, freshness_check

def test_yaml_checks():
    engine = load_sqlite(os.getenv("DQ_DB_PATH", "dq_local.db"))
    specs = load_specs()

    for spec in specs:
        for check in spec.get("checks", []):
            ctype = check["type"]

            if ctype == "nulls":
                result = nulls_check(
                    engine,
                    table=check["table"],
                    column=check["column"],
                    max_null_pct=check.get("max_null_pct", 0.0),
                )
                assert result.passed, f"{check['id']}: {result.message}"

            elif ctype == "uniqueness":
                result = uniqueness_check(
                    engine,
                    table=check["table"],
                    column=check["column"],
                    max_dupes=check.get("max_dupes", 0),
                )
                assert result.passed, f"{check['id']}: {result.message}"

            elif ctype == "referential":
                result = referential_check(
                    engine,
                    source_table=check["source_table"],
                    source_column=check["source_column"],
                    target_table=check["target_table"],
                    target_column=check["target_column"],
                    max_violations=check.get("max_violations", 0),
                )
                assert result.passed, f"{check['id']}: {result.message}"

            elif ctype == "freshness":
                result = freshness_check(
                    engine,
                    table=check["table"],
                    ts_col=check["ts_col"],
                    max_age_hours=float(check.get("max_age_hours", 24)),
                )
                assert result.passed, f"{check['id']}: {result.message}"

            else:
                raise ValueError(f"Unknown check type: {ctype}")
