from auth.password import hash_password, verify_password
from database.database import get_connection


def list_users() -> list[dict]:
    query = """
        SELECT
            u.id,
            u.username,
            u.email,
            u.full_name,
            u.is_active,
            IFNULL(GROUP_CONCAT(r.name, ', '), '') AS roles,
            IFNULL(
                (
                    SELECT GROUP_CONCAT(DISTINCT c.name)
                    FROM company_users cu
                    JOIN companies c ON c.id = cu.company_id
                    WHERE cu.user_id = u.id
                ),
                ''
            ) AS companies,
            IFNULL(
                (
                    SELECT GROUP_CONCAT(DISTINCT csr.name)
                    FROM company_user_subroles cus
                    JOIN company_subroles csr ON csr.id = cus.subrole_id
                    WHERE cus.user_id = u.id
                ),
                ''
            ) AS subroles,
            u.created_at
        FROM users u
        LEFT JOIN user_roles ur ON ur.user_id = u.id
        LEFT JOIN roles r ON r.id = ur.role_id
        GROUP BY u.id
        ORDER BY u.id DESC
    """
    with get_connection() as connection:
        rows = connection.execute(query).fetchall()
    return [dict(row) for row in rows]


def create_user(
    username: str,
    email: str,
    full_name: str,
    password: str,
    company_id: int | None = None,
    subrole_id: int | None = None,
    is_company_admin: bool = False,
) -> bool:
    if not username.strip() or not password.strip():
        return False

    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO users(username, email, full_name, password_hash, is_active)
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    username.strip().lower(),
                    email.strip(),
                    full_name.strip(),
                    hash_password(password),
                ),
            )
            user_id = cursor.lastrowid

            if company_id:
                connection.execute(
                    """
                    INSERT OR IGNORE INTO company_users(company_id, user_id, is_company_admin)
                    VALUES (?, ?, ?)
                    """,
                    (company_id, user_id, 1 if is_company_admin else 0),
                )

                if subrole_id:
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


def authenticate_user(username: str, password: str) -> dict | None:
    query = """
        SELECT
            u.id,
            u.username,
            u.email,
            u.full_name,
            u.password_hash,
            u.is_active,
            IFNULL(GROUP_CONCAT(DISTINCT r.name), '') AS roles,
            IFNULL(
                (
                    SELECT GROUP_CONCAT(DISTINCT c.name)
                    FROM company_users cu
                    JOIN companies c ON c.id = cu.company_id
                    WHERE cu.user_id = u.id
                ),
                ''
            ) AS companies,
            IFNULL(
                (
                    SELECT GROUP_CONCAT(DISTINCT csr.name)
                    FROM company_user_subroles cus
                    JOIN company_subroles csr ON csr.id = cus.subrole_id
                    WHERE cus.user_id = u.id
                ),
                ''
            ) AS subroles
        FROM users u
        LEFT JOIN user_roles ur ON ur.user_id = u.id
        LEFT JOIN roles r ON r.id = ur.role_id
        WHERE u.username = ?
        GROUP BY u.id
        LIMIT 1
    """

    with get_connection() as connection:
        row = connection.execute(query, (username.strip().lower(),)).fetchone()

    if row is None:
        return None

    user = dict(row)
    if not user.get("is_active"):
        return None

    if not verify_password(password, user["password_hash"]):
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "is_active": bool(user["is_active"]),
        "roles": [role.strip() for role in user.get("roles", "").split(",") if role.strip()],
        "companies": [name.strip() for name in user.get("companies", "").split(",") if name.strip()],
        "subroles": [name.strip() for name in user.get("subroles", "").split(",") if name.strip()],
    }


def update_user(user_id: int, **kwargs) -> bool:
    """Actualiza campos de un usuario"""
    allowed_fields = {'email', 'full_name', 'is_active', 'password_hash'}
    
    # Convertir password a password_hash si viene password
    updates = {}
    for key, value in kwargs.items():
        if key == 'password' and value:
            updates['password_hash'] = hash_password(value)
        elif key in allowed_fields and key != 'password':
            updates[key] = value
    
    if not updates:
        return False
    
    with get_connection() as connection:
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [user_id]
        
        connection.execute(
            f"UPDATE users SET {set_clause} WHERE id = ?",
            values
        )
        connection.commit()
        return True


def delete_user(user_id: int) -> bool:
    """Elimina un usuario (y sus relaciones)"""
    with get_connection() as connection:
        try:
            # Eliminar relaciones primero
            connection.execute("DELETE FROM user_roles WHERE user_id = ?", (user_id,))
            connection.execute("DELETE FROM company_users WHERE user_id = ?", (user_id,))
            connection.execute("DELETE FROM company_user_subroles WHERE user_id = ?", (user_id,))
            
            # Eliminar usuario
            connection.execute("DELETE FROM users WHERE id = ?", (user_id,))
            connection.commit()
            return True
        except Exception:
            return False


def get_user_by_id(user_id: int) -> dict:
    """Obtiene un usuario por ID"""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, username, email, full_name, is_active FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    return dict(row) if row else None
