from database.database import get_connection


def list_roles() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, description, created_at FROM roles ORDER BY name"
        ).fetchall()
    return [dict(row) for row in rows]


def get_role_by_id(role_id: int) -> dict:
    """Obtiene un rol por ID"""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, name, description FROM roles WHERE id = ?",
            (role_id,)
        ).fetchone()
    return dict(row) if row else None


def create_role(name: str, description: str = "") -> bool:
    if not name.strip():
        return False
    with get_connection() as connection:
        try:
            connection.execute(
                "INSERT INTO roles(name, description) VALUES (?, ?)",
                (name.strip().lower(), description.strip()),
            )
            return True
        except Exception:
            return False


def update_role(role_id: int, name: str = None, description: str = None) -> bool:
    """Actualiza un rol"""
    updates = {}
    if name:
        updates['name'] = name.strip().lower()
    if description is not None:
        updates['description'] = description.strip()
    
    if not updates:
        return False
    
    with get_connection() as connection:
        try:
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [role_id]
            connection.execute(
                f"UPDATE roles SET {set_clause} WHERE id = ?",
                values
            )
            connection.commit()
            return True
        except Exception:
            return False


def delete_role(role_id: int) -> bool:
    """Elimina un rol (y sus asignaciones)"""
    with get_connection() as connection:
        try:
            connection.execute("DELETE FROM user_roles WHERE role_id = ?", (role_id,))
            connection.execute("DELETE FROM roles WHERE id = ?", (role_id,))
            connection.commit()
            return True
        except Exception:
            return False


def assign_role(user_id: int, role_id: int) -> bool:
    with get_connection() as connection:
        try:
            connection.execute(
                "INSERT OR IGNORE INTO user_roles(user_id, role_id) VALUES (?, ?)",
                (user_id, role_id),
            )
            return True
        except Exception:
            return False
