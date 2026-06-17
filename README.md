# OPRIA OS MVP

Boilerplate base para un MVP con Streamlit + SQLite, con autenticacion, roles, procesos y dashboards administrativos.

Incluye soporte multiempresa (SaaS):

- Empresas (`companies`)
- Relacion usuario-empresa (`company_users`)
- Subroles por empresa (`company_subroles`)
- Asignacion de subroles por usuario en empresa (`company_user_subroles`)

## Estructura

```text
opria_os_mvp/
|
+-- app.py
+-- config.py
+-- requirements.txt
+-- README.md
|
+-- database/
|   +-- database.py
|   +-- init_db.py
|   +-- opria.db
|
+-- auth/
|   +-- jwt_manager.py
|   +-- password.py
|   +-- session.py
|
+-- models/
|   +-- user.py
|   +-- role.py
|   +-- company.py
|   +-- process.py
|
+-- services/
|   +-- user_service.py
|   +-- role_service.py
|   +-- company_service.py
|   +-- process_service.py
|
+-- dashboards/
|   +-- main_dashboard.py
|   |
|   +-- admin/
|       +-- companies.py
|       +-- users.py
|       +-- roles.py
|       +-- processes.py
|
+-- components/
|   +-- navigation.py
|   +-- sidebar.py
|   +-- tables.py
|   +-- forms.py
|
+-- utils/
|   +-- validators.py
|   +-- helpers.py
|
+-- assets/
|   +-- logo.png
|   +-- styles.css
```

## Puesta en marcha

1. Instala dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Ejecuta la app:

   ```bash
   streamlit run app.py
   ```

3. Ejecuta la landing comercial multipagina:

   ```bash
   streamlit run landing.py
   ```

   La landing comercial usa navegacion por botones en el sidebar y esta organizada por modulos en `modules/landing/`.

4. Credenciales iniciales:

   - Usuario: `admin`
   - Password: `Admin123!`

## Notas

- La base de datos se inicializa automaticamente al arrancar.
- `database/opria.db` se crea si no existe.
