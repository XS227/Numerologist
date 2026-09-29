from __future__ import annotations

import re
import sqlite3
from pathlib import Path
from typing import Any

from django.conf import settings

from .catalog import PACKAGE_CATALOG


def _db_path() -> Path:
    return Path(settings.BASE_DIR) / "data" / "orders.db"


def _norm_phone(value: str) -> str:
    digits = re.sub(r"\D", "", value or "")
    if len(digits) == 10 and digits.startswith("47"):
        digits = digits[2:]
    return digits


def _rows_for_identity(email: str = "", phone: str = "") -> list[dict[str, Any]]:
    db = _db_path()
    if not db.exists():
        return []
    email = (email or "").strip().lower()
    phone = _norm_phone(phone)
    conn = sqlite3.connect(str(db))
    conn.row_factory = sqlite3.Row
    try:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(orders)").fetchall()}
        notes_expr = "COALESCE(notes, '') AS notes" if "notes" in columns else "'' AS notes"
        rows = conn.execute(
            f"""
            SELECT id, package, price_ore, birth_name, current_name, birth_date,
                   address, phone, email, payment_status, analysis_status,
                   created_at, {notes_expr}
              FROM orders
             ORDER BY created_at DESC
            """
        ).fetchall()
    finally:
        conn.close()
    result: list[dict[str, Any]] = []
    for row in rows:
        row_email = (row["email"] or "").strip().lower()
        row_phone = _norm_phone(row["phone"] or "")
        if email and row_email == email:
            result.append(dict(row))
        elif phone and row_phone and row_phone == phone:
            result.append(dict(row))
    return result


def orders_for_user(user) -> list[dict[str, Any]]:
    profile = getattr(user, "numerologist_profile", None)
    phone = getattr(profile, "phone", "") if profile else ""
    rows = _rows_for_identity(getattr(user, "email", ""), phone)
    for row in rows:
        product = PACKAGE_CATALOG.get(row["package"], {})
        row["product"] = product
        row["title"] = product.get("title", row["package"])
        row["price"] = row["price_ore"] / 100
        row["digital_available"] = row["payment_status"] in {"paid", "captured", "complete", "completed"}
    return rows


def order_for_user(user, order_id: str) -> dict[str, Any] | None:
    for row in orders_for_user(user):
        if row["id"] == order_id:
            return row
    return None
