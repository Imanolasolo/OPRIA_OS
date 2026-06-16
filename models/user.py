from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool = True
    roles: list[str] = field(default_factory=list)
