from database.database import get_connection
from models.sales_report import SalesReport


def create_sales_report(
    company_id: int,
    user_id: int,
    report_date: str,
    branch: str,
    salesman_name: str,
    customer_name: str,
    tire_brand: str,
    tire_model: str,
    quantity: int,
    unit_price: float,
    payment_method: str,
    observations: str = "",
) -> int:
    """Crea un nuevo reporte de ventas"""
    total_price = quantity * unit_price
    
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO sales_reports (
                company_id, user_id, report_date, branch, 
                salesman_name, customer_name, tire_brand, tire_model,
                quantity, unit_price, total_price, payment_method, observations
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                company_id, user_id, report_date, branch,
                salesman_name, customer_name, tire_brand, tire_model,
                quantity, unit_price, total_price, payment_method, observations
            ),
        )
        connection.commit()
        return cursor.lastrowid


def list_sales_reports(company_id: int, user_id: int = None, date: str = None) -> list:
    """Lista reportes de ventas - opcionalmente filtrados por usuario y fecha"""
    with get_connection() as connection:
        cursor = connection.cursor()
        
        query = "SELECT * FROM sales_reports WHERE company_id = ?"
        params = [company_id]
        
        if user_id:
            query += " AND user_id = ?"
            params.append(user_id)
        
        if date:
            query += " AND report_date = ?"
            params.append(date)
        
        query += " ORDER BY created_at DESC"
        cursor.execute(query, params)
        
        rows = cursor.fetchall()
        return [SalesReport.from_row(row) for row in rows]


def get_sales_report(report_id: int) -> SalesReport:
    """Obtiene un reporte de ventas por ID"""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM sales_reports WHERE id = ?", (report_id,))
        row = cursor.fetchone()
        
        if row:
            return SalesReport.from_row(row)
        return None


def update_sales_report_status(report_id: int, status: str) -> bool:
    """Actualiza el estado de un reporte (pending, validated, rejected)"""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE sales_reports SET status = ? WHERE id = ?",
            (status, report_id)
        )
        connection.commit()
        return cursor.rowcount > 0


def update_sales_report(report_id: int, **kwargs) -> bool:
    """Actualiza campos de un reporte de ventas"""
    allowed_fields = {
        'report_date', 'branch', 'salesman_name', 'customer_name',
        'tire_brand', 'tire_model', 'quantity', 'unit_price',
        'payment_method', 'observations', 'status'
    }
    
    update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not update_fields:
        return False
    
    # Recalcular total_price si cambió quantity o unit_price
    if 'quantity' in update_fields or 'unit_price' in update_fields:
        report = get_sales_report(report_id)
        quantity = update_fields.get('quantity', report.quantity)
        unit_price = update_fields.get('unit_price', report.unit_price)
        update_fields['total_price'] = quantity * unit_price
    
    with get_connection() as connection:
        cursor = connection.cursor()
        
        set_clause = ", ".join([f"{k} = ?" for k in update_fields.keys()])
        values = list(update_fields.values()) + [report_id]
        
        cursor.execute(
            f"UPDATE sales_reports SET {set_clause} WHERE id = ?",
            values
        )
        connection.commit()
        return cursor.rowcount > 0


def delete_sales_report(report_id: int) -> bool:
    """Elimina un reporte de ventas"""
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sales_reports WHERE id = ?", (report_id,))
        connection.commit()
        return cursor.rowcount > 0


def get_daily_summary(company_id: int, report_date: str) -> dict:
    """Resumen diario de ventas"""
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_reports,
                SUM(quantity) as total_units,
                SUM(total_price) as total_sales
            FROM sales_reports 
            WHERE company_id = ? AND report_date = ? AND status = 'validated'
            """,
            (company_id, report_date)
        )
        
        row = cursor.fetchone()
        return {
            'total_reports': row[0] or 0,
            'total_units': row[1] or 0,
            'total_sales': row[2] or 0.0,
        }


def get_weekly_summary(company_id: int, start_date: str, end_date: str) -> dict:
    """Resumen semanal de ventas por día"""
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(
            """
            SELECT 
                report_date,
                COUNT(*) as reports,
                SUM(quantity) as units,
                SUM(total_price) as sales
            FROM sales_reports 
            WHERE company_id = ? AND report_date BETWEEN ? AND ? AND status = 'validated'
            GROUP BY report_date
            ORDER BY report_date
            """,
            (company_id, start_date, end_date)
        )
        
        rows = cursor.fetchall()
        return [
            {
                'date': row[0],
                'reports': row[1],
                'units': row[2],
                'sales': row[3],
            }
            for row in rows
        ]
