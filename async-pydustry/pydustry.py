from time import time
from struct import unpack
from socket import socket, create_connection, AF_INET, SOCK_DGRAM
from typing import Tuple

from .utils import run_in_executor, Status


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

    def _get_status(
            self,
            timeout: float,
            encoding: str,
            errors: str
    ) -> Status:
        info = {}
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(self.server)
        s.settimeout(timeout)
        s_time = time()
        s.send(b"\xfe\x01")
        data = s.recv(1024)
        e_time = time()
        s.close()
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
        result = await run_in_executor(self._get_status, timeout, encoding, errors)
        return result

    def _send_command(self, command: str, timeout: float) -> None:
        s = create_connection(self.input_server, timeout=timeout)
        s.sendall(command.encode())
        s.close()

    async def send_command(
            self,
            command: str,
            timeout: float = 5.0,
    ) -> None:
        return await run_in_executor(self._send_command, command, timeout)

    def _ping(self, timeout: float) -> int:
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(self.server)
        s.settimeout(timeout)
        s_time = time()
        s.send(b"\xfe\x01")
        s.recv(1024)
        e_time = time()
        s.close()
        return round((e_time - s_time) * 1000)

    async def ping(
            self,
            timeout: float = 5.0,
    ) -> int:
        result = await run_in_executor(self._ping, timeout)
        return result
