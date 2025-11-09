import os
from dq_core.load_seed import load_sqlite
from dq_core.checks import uniqueness_check

def test_orders_order_id_unique():
    engine = load_sqlite(os.getenv("DQ_DB_PATH", "dq_local.db"))
    result = uniqueness_check(engine, table="orders", column="order_id", max_dupes=0)
    assert result.passed, result.message
