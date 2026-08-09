from zelda.mobile.transport import LocalTransport, TransportFrame


def test_transport_round_trip():
    transport = LocalTransport()
    seen = []
    transport.on_frame(seen.append)
    frame = TransportFrame("COMMAND", "req-1", {"command": "ping"})
    transport.inject(frame)
    assert seen == [frame]
    assert TransportFrame.decode(frame.encode()) == frame
    transport.send(TransportFrame("PONG"))
    assert transport.receive().kind == "PONG"
