from datetime import datetime

from backend.database import DEFAULT_DB_PATH, get_connection, initialize_database
from backend.models import FoundItem, InvalidItemError, LostItem, RecordNotFoundError


class LostFoundService:
    def __init__(self, db_path=DEFAULT_DB_PATH):
        self.db_path = db_path
        initialize_database(db_path)

    def report_item(self, kind, title, description, location, contact, reporter):
        kind = kind.strip().title()
        if kind not in {"Lost", "Found"}:
            raise InvalidItemError("Choose Lost or Found for the report type.")
        values = [title.strip(), description.strip(), location.strip(), contact.strip(), reporter.strip()]
        if not all(values):
            raise InvalidItemError("Complete every report field before submitting.")
        item_class = LostItem if kind == "Lost" else FoundItem
        item = item_class(values[0], values[1], values[2], values[3])
        with get_connection(self.db_path) as connection:
            cursor = connection.execute(
                "INSERT INTO items (kind, title, description, location, contact, reporter, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (kind, item.title, item.description, item.location, item.contact, values[4], item.created_at),
            )
            return cursor.lastrowid

    def list_items(self, kind="All", status="Open", query=""):
        clauses = []
        params = []
        if kind in {"Lost", "Found"}:
            clauses.append("kind = ?")
            params.append(kind)
        if status != "All":
            clauses.append("status = ?")
            params.append(status)
        if query.strip():
            pattern = f"%{query.strip()}%"
            clauses.append("(title LIKE ? OR description LIKE ? OR location LIKE ?)")
            params.extend([pattern, pattern, pattern])
        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        with get_connection(self.db_path) as connection:
            return connection.execute(f"SELECT * FROM items {where} ORDER BY created_at DESC", params).fetchall()

    def close_item(self, item_id):
        try:
            parsed_id = int(item_id)
        except (TypeError, ValueError) as error:
            raise InvalidItemError("Enter a valid numeric item ID.") from error
        if parsed_id < 1:
            raise InvalidItemError("Item ID must be a positive number.")
        with get_connection(self.db_path) as connection:
            cursor = connection.execute("UPDATE items SET status = 'Resolved' WHERE id = ? AND status = 'Open'", (parsed_id,))
            if cursor.rowcount == 0:
                exists = connection.execute("SELECT status FROM items WHERE id = ?", (parsed_id,)).fetchone()
                if exists is None:
                    raise RecordNotFoundError(f"No item with ID {parsed_id} exists.")
                raise RecordNotFoundError(f"Item {parsed_id} is already resolved.")

    def total_count(self):
        with get_connection(self.db_path) as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM items").fetchone()
            return row["total"]
