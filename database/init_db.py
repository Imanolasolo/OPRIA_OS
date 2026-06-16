from auth.password import hash_password
from database.database import get_connection


def ensure_database() -> None:
    with get_connection() as connection:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                full_name TEXT,
                password_hash TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_roles (
                user_id INTEGER NOT NULL,
                role_id INTEGER NOT NULL,
                PRIMARY KEY (user_id, role_id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(role_id) REFERENCES roles(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS processes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner TEXT,
                status TEXT NOT NULL DEFAULT 'draft',
                priority TEXT NOT NULL DEFAULT 'medium',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                slug TEXT UNIQUE,
                is_active INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS company_subroles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(company_id, name),
                FOREIGN KEY(company_id) REFERENCES companies(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS company_users (
                company_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                is_company_admin INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(company_id, user_id),
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS company_user_subroles (
                company_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                subrole_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(company_id, user_id, subrole_id),
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(user_id) REFERENCES users(id),
                FOREIGN KEY(subrole_id) REFERENCES company_subroles(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sales_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                report_date TEXT NOT NULL,
                branch TEXT NOT NULL,
                salesman_name TEXT NOT NULL,
                customer_name TEXT NOT NULL,
                tire_brand TEXT NOT NULL,
                tire_model TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                payment_method TEXT NOT NULL,
                observations TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS process_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                schema_json TEXT,
                version INTEGER NOT NULL DEFAULT 1,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name, version)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS process_type_permissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_type_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                role_id INTEGER,
                subrole_id INTEGER,
                can_create INTEGER NOT NULL DEFAULT 0,
                can_validate INTEGER NOT NULL DEFAULT 0,
                can_close INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(process_type_id, company_id, role_id, subrole_id),
                FOREIGN KEY(process_type_id) REFERENCES process_types(id),
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(role_id) REFERENCES roles(id),
                FOREIGN KEY(subrole_id) REFERENCES company_subroles(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS process_instances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_type_id INTEGER NOT NULL,
                company_id INTEGER NOT NULL,
                created_by_user_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'draft',
                payload_json TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(process_type_id) REFERENCES process_types(id),
                FOREIGN KEY(company_id) REFERENCES companies(id),
                FOREIGN KEY(created_by_user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS process_instance_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_instance_id INTEGER NOT NULL,
                from_status TEXT,
                to_status TEXT NOT NULL,
                action TEXT NOT NULL,
                comment TEXT,
                changed_by_user_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(process_instance_id) REFERENCES process_instances(id),
                FOREIGN KEY(changed_by_user_id) REFERENCES users(id)
            )
            """
        )

        cursor.execute("INSERT OR IGNORE INTO roles(name, description) VALUES ('admin', 'Administrador')")
        cursor.execute("INSERT OR IGNORE INTO roles(name, description) VALUES ('user', 'Usuario')")

        cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin_user = cursor.fetchone()

        if admin_user is None:
            cursor.execute(
                """
                INSERT INTO users(username, email, full_name, password_hash, is_active)
                VALUES (?, ?, ?, ?, 1)
                """,
                ("admin", "admin@opria.local", "Administrador", hash_password("Admin123!")),
            )
            admin_user_id = cursor.lastrowid
            cursor.execute("SELECT id FROM roles WHERE name = 'admin'")
            admin_role_id = cursor.fetchone()[0]
            cursor.execute(
                "INSERT OR IGNORE INTO user_roles(user_id, role_id) VALUES (?, ?)",
                (admin_user_id, admin_role_id),
            )

        cursor.execute(
            "INSERT OR IGNORE INTO companies(name, slug, is_active) VALUES ('OPRIA Demo', 'opria-demo', 1)"
        )
        cursor.execute("SELECT id FROM companies WHERE slug = 'opria-demo'")
        demo_company_id = cursor.fetchone()[0]

        for subrole_name, subrole_description in [
            ("owner", "Propietario de la empresa"),
            ("manager", "Responsable operativo"),
            ("analyst", "Analista de negocio"),
            ("operator", "Operador de procesos"),
        ]:
            cursor.execute(
                """
                INSERT OR IGNORE INTO company_subroles(company_id, name, description)
                VALUES (?, ?, ?)
                """,
                (demo_company_id, subrole_name, subrole_description),
            )

        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        admin_user_id = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT OR IGNORE INTO company_users(company_id, user_id, is_company_admin)
            VALUES (?, ?, 1)
            """,
            (demo_company_id, admin_user_id),
        )

        cursor.execute(
            "SELECT id FROM company_subroles WHERE company_id = ? AND name = 'owner'",
            (demo_company_id,),
        )
        owner_subrole_id = cursor.fetchone()[0]
        cursor.execute(
            """
            INSERT OR IGNORE INTO company_user_subroles(company_id, user_id, subrole_id)
            VALUES (?, ?, ?)
            """,
            (demo_company_id, admin_user_id, owner_subrole_id),
        )
