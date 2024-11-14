from dataclasses import dataclass


@dataclass
class Status:
    name: str
    map: str
    players: int
    wave: int
    version: float
    vertype: str
    gamemode: int
    limit: int
    desc: int
    modename: int
    ping: int
