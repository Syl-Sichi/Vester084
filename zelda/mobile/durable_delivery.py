from zelda.mobile.ack import AckTracker
from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.transport import TransportFrame


class DurableMobileDelivery:
    """Coordinates durable events and acknowledgements for one mobile client."""

    def __init__(self, journal: MobileEventJournal, ack: AckTracker | None = None) -> None:
        self.journal = journal
        self.ack = ack or AckTracker()

    def record(self, frame: TransportFrame):
        return self.journal.append(frame)

    def acknowledge(self, sequence: int) -> int:
        return self.ack.acknowledge(sequence)

    def pending(self):
        return self.journal.after(self.ack.acknowledged)

    def replay(self) -> list[TransportFrame]:
        return [item.frame for item in self.pending()]
