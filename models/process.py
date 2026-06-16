from dataclasses import dataclass


@dataclass
class Process:
    id: int
    name: str
    owner: str
    status: str
    priority: str
