from dataclasses import dataclass

from zelda.mobile.durable_delivery import DurableMobileDelivery


@dataclass(frozen=True)
class SyncResult:
    acknowledged: int
    replay: list


class MobileSyncProtocol:
    """Handles reconnect synchronization for an authenticated mobile client."""

    def __init__(self, delivery: DurableMobileDelivery) -> None:
        self.delivery = delivery

    def hello(self, last_acknowledged: int = 0) -> SyncResult:
        acknowledged = self.delivery.acknowledge(last_acknowledged)
        return SyncResult(acknowledged, self.delivery.replay())

    def ack(self, sequence: int) -> int:
        return self.delivery.acknowledge(sequence)
