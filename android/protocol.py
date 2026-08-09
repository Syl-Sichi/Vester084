from dataclasses import dataclass

from zelda.mobile.transport import TransportFrame


@dataclass(frozen=True)
class AndroidCommand:
    request_id: str
    command: str

    def frame(self, access_token: str) -> TransportFrame:
        return TransportFrame(
            "COMMAND",
            self.request_id,
            {"access_token": access_token, "command": self.command},
        )


@dataclass(frozen=True)
class AndroidHello:
    request_id: str
    access_token: str
    last_acknowledged: int

    def frame(self) -> TransportFrame:
        return TransportFrame(
            "HELLO",
            self.request_id,
            {
                "access_token": self.access_token,
                "last_acknowledged": self.last_acknowledged,
            },
        )


@dataclass(frozen=True)
class AndroidAck:
    request_id: str
    access_token: str
    sequence: int

    def frame(self) -> TransportFrame:
        return TransportFrame(
            "ACK",
            self.request_id,
            {"access_token": self.access_token, "sequence": self.sequence},
        )
