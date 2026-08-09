import queue
import threading
from dataclasses import dataclass

from zelda.mobile.transport import LocalTransport, TransportFrame


@dataclass(frozen=True)
class DeliveryItem:
    sequence: int
    frame: TransportFrame


class MobileDeliveryQueue:
    """Bounded in memory event queue with monotonically increasing sequence IDs."""

    def __init__(self, max_items: int = 256) -> None:
        if max_items < 1:
            raise ValueError("max_items must be positive")
        self._queue: queue.Queue[DeliveryItem] = queue.Queue(maxsize=max_items)
        self._sequence = 0
        self._lock = threading.Lock()

    def enqueue(self, frame: TransportFrame) -> DeliveryItem:
        with self._lock:
            self._sequence += 1
            item = DeliveryItem(self._sequence, frame)
        self._queue.put_nowait(item)
        return item

    def next(self, timeout: float | None = None) -> DeliveryItem:
        return self._queue.get(timeout=timeout)

    def size(self) -> int:
        return self._queue.qsize()


class MobileEventDelivery:
    """Queues outbound mobile events before the transport sends them."""

    def __init__(self, transport: LocalTransport, max_items: int = 256) -> None:
        self.transport = transport
        self.queue = MobileDeliveryQueue(max_items)
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="zelda-mobile-delivery", daemon=True)

    def start(self) -> None:
        if not self._thread.is_alive():
            self._thread.start()

    def publish(self, frame: TransportFrame) -> DeliveryItem:
        return self.queue.enqueue(frame)

    def stop(self) -> None:
        self._stop.set()
        if self._thread.is_alive():
            self._thread.join(timeout=1)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                item = self.queue.next(timeout=0.1)
            except queue.Empty:
                continue
            self.transport.send(item.frame)
