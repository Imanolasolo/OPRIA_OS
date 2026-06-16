from dataclasses import dataclass


@dataclass
class SalesReport:
    """Modelo para reportes de ventas de neumáticos"""
    id: int
    company_id: int
    user_id: int
    report_date: str
    branch: str
    salesman_name: str
    customer_name: str
    tire_brand: str
    tire_model: str
    quantity: int
    unit_price: float
    total_price: float
    payment_method: str
    observations: str = ""
    status: str = "pending"
    created_at: str = ""

    @classmethod
    def from_row(cls, row):
        """Crea un SalesReport desde una fila de base de datos"""
        return cls(
            id=row[0],
            company_id=row[1],
            user_id=row[2],
            report_date=row[3],
            branch=row[4],
            salesman_name=row[5],
            customer_name=row[6],
            tire_brand=row[7],
            tire_model=row[8],
            quantity=row[9],
            unit_price=row[10],
            total_price=row[11],
            payment_method=row[12],
            observations=row[13] or "",
            status=row[14],
            created_at=row[15],
        )
