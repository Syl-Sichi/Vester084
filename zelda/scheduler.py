import threading
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

from zelda.events.bus import Event, EventBus


@dataclass
class ScheduledJob:
    id: str
    run_at: float
    topic: str
    payload: dict
    repeat_seconds: float | None = None


class Scheduler:
    """Small in process scheduler for trusted event producers."""

    def __init__(self, event_bus: EventBus) -> None:
        self.event_bus = event_bus
        self.jobs: dict[str, ScheduledJob] = {}
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def schedule(self, run_at: datetime, topic: str, payload: dict | None = None, repeat_seconds: float | None = None) -> str:
        if run_at.tzinfo is None:
            raise ValueError("run_at must be timezone aware")
        job_id = uuid.uuid4().hex
        self.jobs[job_id] = ScheduledJob(job_id, run_at.timestamp(), topic, payload or {}, repeat_seconds)
        return job_id

    def cancel(self, job_id: str) -> bool:
        return self.jobs.pop(job_id, None) is not None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="zelda-scheduler", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _loop(self) -> None:
        while not self._stop.wait(0.25):
            now = time.time()
            for job_id, job in list(self.jobs.items()):
                if now < job.run_at:
                    continue
                self.event_bus.publish(Event(job.topic, {"job_id": job.id, **job.payload}))
                if job.repeat_seconds and job.repeat_seconds > 0:
                    job.run_at = now + job.repeat_seconds
                else:
                    self.jobs.pop(job_id, None)
