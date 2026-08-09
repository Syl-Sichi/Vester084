from zelda.events.bus import Event, EventBus
from zelda.mobile.transport import LocalTransport, TransportFrame


class MobileEventBridge:
    """Forward selected Z.E.L.D.A. events to an authenticated mobile transport."""

    def __init__(self, event_bus: EventBus, transport: LocalTransport, allowed_topics: set[str] | None = None) -> None:
        self.transport = transport
        self.allowed_topics = allowed_topics or {
            "message.received",
            "notification.received",
            "task.completed",
            "workflow.completed",
            "system.alert",
        }
        for topic in self.allowed_topics:
            event_bus.subscribe(topic, self.publish)

    def publish(self, event: Event) -> None:
        self.transport.send(
            TransportFrame(
                "EVENT",
                payload={
                    "topic": event.topic,
                    "payload": event.payload,
                    "created_at": event.created_at,
                },
            )
        )
