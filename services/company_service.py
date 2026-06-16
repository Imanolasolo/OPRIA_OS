from database.database import get_connection


def list_companies() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, name, slug, is_active, created_at
            FROM companies
            ORDER BY name
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_company_by_name(name: str) -> dict:
    """Obtiene una empresa por nombre"""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, name, slug, is_active, created_at FROM companies WHERE name = ? LIMIT 1",
            (name,)
        ).fetchone()
    
    return dict(row) if row else None


def get_company_id_by_name(name: str) -> int:
    """Obtiene solo el ID de una empresa por nombre"""
    company = get_company_by_name(name)
    return company['id'] if company else None


def create_company(name: str, slug: str = "") -> bool:
    if not name.strip():
        return False

    safe_slug = (slug or "").strip().lower().replace(" ", "-")
    if not safe_slug:
        safe_slug = name.strip().lower().replace(" ", "-")

    with get_connection() as connection:
        try:
            connection.execute(
                "INSERT INTO companies(name, slug, is_active) VALUES (?, ?, 1)",
                (name.strip(), safe_slug),
            )
            return True
        except Exception:
            return False


def list_company_subroles(company_id: int) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, company_id, name, description, created_at
            FROM company_subroles
            WHERE company_id = ?
            ORDER BY name
            """,
            (company_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def create_company_subrole(company_id: int, name: str, description: str = "") -> bool:
    if not company_id or not name.strip():
        return False

    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT INTO company_subroles(company_id, name, description)
                VALUES (?, ?, ?)
                """,
                (company_id, name.strip().lower(), description.strip()),
            )
            return True
        except Exception:
            return False


def assign_user_to_company(user_id: int, company_id: int, is_company_admin: bool = False) -> bool:
    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT OR IGNORE INTO company_users(company_id, user_id, is_company_admin)
                VALUES (?, ?, ?)
                """,
                (company_id, user_id, 1 if is_company_admin else 0),
            )
            return True
        except Exception:
            return False


def assign_subrole_to_user(user_id: int, company_id: int, subrole_id: int) -> bool:
    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT OR IGNORE INTO company_user_subroles(company_id, user_id, subrole_id)
                VALUES (?, ?, ?)
                """,
                (company_id, user_id, subrole_id),
            )
            return True
        except Exception:
            return False


def update_company(company_id: int, name: str = None, slug: str = None) -> bool:
    """Actualiza una empresa"""
    updates = {}
    if name:
        updates['name'] = name.strip()
    if slug:
        updates['slug'] = slug.strip().lower().replace(" ", "-")
    
    if not updates:
        return False
    
    with get_connection() as connection:
        try:
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [company_id]
            connection.execute(
                f"UPDATE companies SET {set_clause} WHERE id = ?",
                values
            )
            connection.commit()
            return True
        except Exception:
            return False


def delete_company(company_id: int) -> bool:
    """Elimina una empresa (y todas sus relaciones)"""
    with get_connection() as connection:
        try:
            # Eliminar relaciones de usuarios con la empresa
            connection.execute("DELETE FROM company_users WHERE company_id = ?", (company_id,))
            connection.execute("DELETE FROM company_user_subroles WHERE company_id = ?", (company_id,))
            
            # Eliminar subroles
            connection.execute("DELETE FROM company_subroles WHERE company_id = ?", (company_id,))
            
            # Eliminar empresa
            connection.execute("DELETE FROM companies WHERE id = ?", (company_id,))
            connection.commit()
            return True
        except Exception:
            return False


def update_company_subrole(subrole_id: int, name: str = None, description: str = None) -> bool:
    """Actualiza un subrol"""
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
            values = list(updates.values()) + [subrole_id]
            connection.execute(
                f"UPDATE company_subroles SET {set_clause} WHERE id = ?",
                values
            )
            connection.commit()
            return True
        except Exception:
            return False


def delete_company_subrole(subrole_id: int) -> bool:
    """Elimina un subrol (y sus asignaciones)"""
    with get_connection() as connection:
        try:
            connection.execute("DELETE FROM company_user_subroles WHERE subrole_id = ?", (subrole_id,))
            connection.execute("DELETE FROM company_subroles WHERE id = ?", (subrole_id,))
            connection.commit()
            return True
        except Exception:
            return False
