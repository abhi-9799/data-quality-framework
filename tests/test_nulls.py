import os
from dq_core.load_seed import load_sqlite
from dq_core.checks import nulls_check

def test_orders_amount_has_no_nulls():
    engine = load_sqlite(os.getenv("DQ_DB_PATH", "dq_local.db"))
    result = nulls_check(engine, table="orders", column="amount", max_null_pct=0.0)
    assert result.passed, result.message
