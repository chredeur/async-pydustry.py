import asyncio
from time import time
from struct import unpack
from socket import socket, AF_INET, SOCK_DGRAM
from typing import Tuple

from .utils import Status


class Server:
    def __init__(
            self,
            server_host: str,
            server_port: int = 6567,
            input_port: int = 6859
    ) -> None:
        self.server: Tuple[str, int] = (server_host, server_port)
        self.input_server: Tuple[str, int] = (server_host, input_port)

    def __str__(self) -> str:
        return f"{self.server[0]}:{self.server[1]}:{self.input_server[1]}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.__str__())})"

    async def _get_status(
            self,
            timeout: float,
            encoding: str,
            errors: str
    ) -> Status:
        info = {}
        loop = asyncio.get_running_loop()

        with socket(AF_INET, SOCK_DGRAM) as s:
            s.setblocking(False)
            s.settimeout(timeout)
            s.connect(self.server)

            s_time = time()
            await asyncio.wait_for(loop.sock_sendto(s, b"\xfe\x01", self.server), timeout=timeout)

            data = await asyncio.wait_for(loop.sock_recv(s, 1024), timeout=timeout)
            e_time = time()

        info['name'] = data[1:data[0] + 1].decode(encoding, errors)
        data = data[data[0] + 1:]
        info['map'] = data[1:data[0] + 1].decode(encoding, errors)
        data = data[data[0] + 1:]
        info['players'] = unpack(">i", data[:4])[0]
        data = data[4:]
        info['wave'] = unpack(">i", data[:4])[0]
        data = data[4:]
        info['version'] = unpack(">i", data[:4])[0]
        data = data[4:]
        info['vertype'] = data[1:data[0] + 1].decode(encoding, errors)
        data = data[data[0] + 1:]
        info['gamemode'] = unpack('>b', data[:1])[0]
        data = data[1:]
        info['limit'] = unpack(">i", data[:4])[0]
        data = data[4:]
        info['desc'] = data[1:data[0] + 1].decode(encoding, errors)
        data = data[data[0] + 1:]
        info['modename'] = data[1:data[0] + 1].decode(encoding, errors)
        data = data[data[0] + 1:]
        info['ping'] = round((e_time - s_time) * 1000)

        return Status(**info)

    async def get_status(
            self,
            timeout: float = 5.0,
            encoding: str = 'utf-8',
            errors: str = 'strict'
    ) -> Status:
        return await self._get_status(timeout, encoding, errors)

    async def _send_command(self, command: str, timeout: float) -> None:
        reader, writer = await asyncio.open_connection(
            self.input_server[0], self.input_server[1]
        )

        writer.write(command.encode())
        await asyncio.wait_for(writer.drain(), timeout=timeout)
        writer.close()
        await writer.wait_closed()

    async def send_command(
            self,
            command: str,
            timeout: float = 5.0,
    ) -> None:
        await asyncio.wait_for(self._send_command(command, timeout), timeout=timeout)

    async def _ping(self, timeout: float) -> int:
        loop = asyncio.get_running_loop()

        with socket(AF_INET, SOCK_DGRAM) as s:
            s.setblocking(False)
            s.settimeout(timeout)
            s.connect(self.server)
            s_time = time()

            await asyncio.wait_for(loop.sock_sendto(s, b"\xfe\x01", self.server), timeout=timeout)

            await asyncio.wait_for(loop.sock_recv(s, 1024), timeout=timeout)
            e_time = time()

        return round((e_time - s_time) * 1000)

    async def ping(
            self,
            timeout: float = 5.0,
    ) -> int:
        return await self._ping(timeout)
