from zelda.events.bus import Event, EventBus
from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.transport import TransportFrame


class DurableMobileEventBridge:
    """Persist approved mobile events before handing them to a delivery callback."""

    DEFAULT_TOPICS = frozenset({
        "message.received",
        "notification.received",
        "task.completed",
        "workflow.completed",
        "system.alert",
    })

    def __init__(self, event_bus: EventBus, journal: MobileEventJournal, deliver, allowed_topics=None) -> None:
        self.journal = journal
        self.deliver = deliver
        self.allowed_topics = frozenset(allowed_topics or self.DEFAULT_TOPICS)
        for topic in self.allowed_topics:
            event_bus.subscribe(topic, self.publish)

    def publish(self, event: Event):
        frame = TransportFrame(
            "EVENT",
            payload={
                "topic": event.topic,
                "payload": event.payload,
                "created_at": event.created_at,
            },
        )
        journal_event = self.journal.append(frame)
        self.deliver(journal_event)
        return journal_event
