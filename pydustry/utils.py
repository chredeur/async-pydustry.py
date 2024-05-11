import asyncio
import functools
from dataclasses import dataclass
from typing import Any


async def run_in_executor(func, *args, **kwargs) -> Any:
    """Run function in executor

    Parameters
    ----------
    func: func
        Function to run
    """
    func = functools.partial(func, *args, **kwargs)
    data = await asyncio.get_event_loop().run_in_executor(None, func)
    return data


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
