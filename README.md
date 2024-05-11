# Installation
```cmd
pip install git+https://github.com/chredeur/pydustry.py
```

# Example
- `main.py`

```python
import asyncio
import async_pydustry


async def main():
    status = async_pydustry.Server("pastanetwork.com").get_status()
    print(status)


asyncio.run(main())
```

- `Return`
```python
Status(
    name='[gold]RCR [#B5B8B1]- [white]Ру[blue]сс[red]кий [#B5B8B1]Сервер',
    map='RCR HUB',
    players=7,
    wave=1,
    version=146,
    vertype='official',
    gamemode=0,
    limit=0,
    desc='...',
    modename='LOBBY',
    ping=37
)
```
