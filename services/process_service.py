import json

from database.database import get_connection


VALID_STATUS = ["draft", "active", "paused", "completed"]
VALID_PRIORITIES = ["low", "medium", "high", "critical"]
VALID_INSTANCE_STATUS = ["draft", "submitted", "validated", "approved", "rejected", "closed"]


def list_processes() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, name, owner, status, priority, created_at FROM processes ORDER BY id DESC"
        ).fetchall()
    return [dict(row) for row in rows]


def create_process(name: str, owner: str, status: str, priority: str) -> bool:
    if not name.strip():
        return False
    if status not in VALID_STATUS or priority not in VALID_PRIORITIES:
        return False

    with get_connection() as connection:
        try:
            connection.execute(
                "INSERT INTO processes(name, owner, status, priority) VALUES (?, ?, ?, ?)",
                (name.strip(), owner.strip(), status, priority),
            )
            return True
        except Exception:
            return False


def update_process_status(process_id: int, new_status: str) -> bool:
    if new_status not in VALID_STATUS:
        return False

    with get_connection() as connection:
        cursor = connection.execute(
            "UPDATE processes SET status = ? WHERE id = ?",
            (new_status, process_id),
        )
    return cursor.rowcount > 0


def get_process_by_id(process_id: int) -> dict:
    """Obtiene un proceso por ID"""
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, name, owner, status, priority, created_at FROM processes WHERE id = ?",
            (process_id,)
        ).fetchone()
    return dict(row) if row else None


def update_process(process_id: int, name: str = None, owner: str = None, 
                   status: str = None, priority: str = None) -> bool:
    """Actualiza un proceso"""
    updates = {}
    
    if name:
        updates['name'] = name.strip()
    if owner:
        updates['owner'] = owner.strip()
    if status:
        if status not in VALID_STATUS:
            return False
        updates['status'] = status
    if priority:
        if priority not in VALID_PRIORITIES:
            return False
        updates['priority'] = priority
    
    if not updates:
        return False
    
    with get_connection() as connection:
        try:
            set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
            values = list(updates.values()) + [process_id]
            connection.execute(
                f"UPDATE processes SET {set_clause} WHERE id = ?",
                values
            )
            connection.commit()
            return True
        except Exception:
            return False


def delete_process(process_id: int) -> bool:
    """Elimina un proceso"""
    with get_connection() as connection:
        try:
            connection.execute("DELETE FROM processes WHERE id = ?", (process_id,))
            connection.commit()
            return True
        except Exception:
            return False


def list_process_types() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, name, description, category, version, is_active, created_at
            FROM process_types
            ORDER BY id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def create_process_type(
    name: str,
    description: str = "",
    category: str = "general",
    schema: dict | None = None,
    version: int = 1,
) -> bool:
    if not name.strip() or version < 1:
        return False

    schema_json = json.dumps(schema or {}, ensure_ascii=False)
    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT INTO process_types(name, description, category, schema_json, version, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
                """,
                (name.strip(), description.strip(), category.strip().lower(), schema_json, version),
            )
            connection.commit()
            return True
        except Exception:
            return False


def grant_process_type_permission(
    process_type_id: int,
    company_id: int,
    role_id: int | None = None,
    subrole_id: int | None = None,
    can_create: bool = False,
    can_validate: bool = False,
    can_close: bool = False,
) -> bool:
    if not process_type_id or not company_id:
        return False

    with get_connection() as connection:
        try:
            connection.execute(
                """
                INSERT OR REPLACE INTO process_type_permissions(
                    id, process_type_id, company_id, role_id, subrole_id, can_create, can_validate, can_close
                )
                VALUES (
                    (
                        SELECT id FROM process_type_permissions
                        WHERE process_type_id = ? AND company_id = ?
                          AND COALESCE(role_id, -1) = COALESCE(?, -1)
                          AND COALESCE(subrole_id, -1) = COALESCE(?, -1)
                    ),
                    ?, ?, ?, ?, ?, ?, ?
                )
                """,
                (
                    process_type_id,
                    company_id,
                    role_id,
                    subrole_id,
                    process_type_id,
                    company_id,
                    role_id,
                    subrole_id,
                    1 if can_create else 0,
                    1 if can_validate else 0,
                    1 if can_close else 0,
                ),
            )
            connection.commit()
            return True
        except Exception:
            return False


def list_process_type_permissions() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                p.id,
                pt.name AS process_type,
                c.name AS company,
                r.name AS role,
                cs.name AS subrole,
                p.can_create,
                p.can_validate,
                p.can_close,
                p.created_at
            FROM process_type_permissions p
            JOIN process_types pt ON pt.id = p.process_type_id
            JOIN companies c ON c.id = p.company_id
            LEFT JOIN roles r ON r.id = p.role_id
            LEFT JOIN company_subroles cs ON cs.id = p.subrole_id
            ORDER BY p.id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def list_available_process_types_for_user(company_id: int, user_id: int) -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT DISTINCT
                pt.id,
                pt.name,
                pt.description,
                pt.category,
                pt.version,
                pt.is_active,
                p.can_create,
                p.can_validate,
                p.can_close
            FROM process_types pt
            JOIN process_type_permissions p ON p.process_type_id = pt.id
            LEFT JOIN user_roles ur ON ur.user_id = ?
            LEFT JOIN company_user_subroles cus ON cus.user_id = ? AND cus.company_id = ?
            WHERE p.company_id = ?
              AND pt.is_active = 1
              AND (
                    p.role_id IS NULL OR p.role_id = ur.role_id
                  )
              AND (
                    p.subrole_id IS NULL OR p.subrole_id = cus.subrole_id
                  )
            ORDER BY pt.name
            """,
            (user_id, user_id, company_id, company_id),
        ).fetchall()
    return [dict(row) for row in rows]


def create_process_instance(
    process_type_id: int,
    company_id: int,
    user_id: int,
    payload: dict | None = None,
) -> int | None:
    available = list_available_process_types_for_user(company_id, user_id)
    can_create = any(
        item["id"] == process_type_id and bool(item.get("can_create"))
        for item in available
    )
    if not can_create:
        return None

    payload_json = json.dumps(payload or {}, ensure_ascii=False)
    with get_connection() as connection:
        try:
            cursor = connection.execute(
                """
                INSERT INTO process_instances(process_type_id, company_id, created_by_user_id, status, payload_json)
                VALUES (?, ?, ?, 'submitted', ?)
                """,
                (process_type_id, company_id, user_id, payload_json),
            )
            instance_id = cursor.lastrowid
            connection.execute(
                """
                INSERT INTO process_instance_events(
                    process_instance_id, from_status, to_status, action, comment, changed_by_user_id
                )
                VALUES (?, NULL, 'submitted', 'create', 'Instancia creada', ?)
                """,
                (instance_id, user_id),
            )
            connection.commit()
            return instance_id
        except Exception:
            return None


def list_process_instances(company_id: int, user_id: int, only_mine: bool = True) -> list[dict]:
    mine_filter = "AND pi.created_by_user_id = ?" if only_mine else ""
    params = [company_id]
    if only_mine:
        params.append(user_id)

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT
                pi.id,
                pi.status,
                pi.payload_json,
                pi.created_at,
                pi.updated_at,
                pt.name AS process_type,
                u.username AS created_by
            FROM process_instances pi
            JOIN process_types pt ON pt.id = pi.process_type_id
            JOIN users u ON u.id = pi.created_by_user_id
            WHERE pi.company_id = ?
            {mine_filter}
            ORDER BY pi.id DESC
            """,
            tuple(params),
        ).fetchall()
    return [dict(row) for row in rows]


def list_process_instances_for_validation(company_id: int, user_id: int) -> list[dict]:
    available = list_available_process_types_for_user(company_id, user_id)
    allowed_type_ids = {
        item["id"]
        for item in available
        if bool(item.get("can_validate")) or bool(item.get("can_close"))
    }
    if not allowed_type_ids:
        return []

    placeholders = ",".join(["?"] * len(allowed_type_ids))
    params = [company_id, *allowed_type_ids]

    with get_connection() as connection:
        rows = connection.execute(
            f"""
            SELECT
                pi.id,
                pi.status,
                pi.payload_json,
                pi.created_at,
                pi.updated_at,
                pt.id AS process_type_id,
                pt.name AS process_type,
                u.username AS created_by
            FROM process_instances pi
            JOIN process_types pt ON pt.id = pi.process_type_id
            JOIN users u ON u.id = pi.created_by_user_id
            WHERE pi.company_id = ?
              AND pi.process_type_id IN ({placeholders})
            ORDER BY pi.id DESC
            """,
            tuple(params),
        ).fetchall()
    return [dict(row) for row in rows]


def update_process_instance_status(
    process_instance_id: int,
    user_id: int,
    company_id: int,
    to_status: str,
    comment: str = "",
) -> bool:
    if to_status not in VALID_INSTANCE_STATUS:
        return False

    with get_connection() as connection:
        instance = connection.execute(
            """
            SELECT id, process_type_id, status
            FROM process_instances
            WHERE id = ? AND company_id = ?
            """,
            (process_instance_id, company_id),
        ).fetchone()

        if not instance:
            return False

        current_status = instance["status"]
        process_type_id = instance["process_type_id"]

        available = list_available_process_types_for_user(company_id, user_id)
        permission = next((item for item in available if item["id"] == process_type_id), None)
        if not permission:
            return False

        can_validate = bool(permission.get("can_validate"))
        can_close = bool(permission.get("can_close"))

        validate_targets = {"validated", "rejected"}
        close_targets = {"approved", "closed"}

        if to_status in validate_targets and not can_validate:
            return False
        if to_status in close_targets and not can_close:
            return False

        try:
            connection.execute(
                """
                UPDATE process_instances
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (to_status, process_instance_id),
            )
            connection.execute(
                """
                INSERT INTO process_instance_events(
                    process_instance_id, from_status, to_status, action, comment, changed_by_user_id
                )
                VALUES (?, ?, ?, 'status_change', ?, ?)
                """,
                (process_instance_id, current_status, to_status, comment.strip(), user_id),
            )
            connection.commit()
            return True
        except Exception:
            return False
