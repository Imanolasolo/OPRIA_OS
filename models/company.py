from dataclasses import dataclass


@dataclass
class Company:
    id: int
    name: str
    slug: str
    is_active: bool = True
