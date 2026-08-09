from android.protocol import AndroidAck, AndroidCommand, AndroidHello


def test_android_command_frame():
    frame = AndroidCommand("cmd-1", "status").frame("token")
    assert frame.kind == "COMMAND"
    assert frame.payload == {"access_token": "token", "command": "status"}


def test_android_hello_frame():
    frame = AndroidHello("hello-1", "token", 12).frame()
    assert frame.kind == "HELLO"
    assert frame.payload["last_acknowledged"] == 12


def test_android_ack_frame():
    frame = AndroidAck("ack-1", "token", 12).frame()
    assert frame.kind == "ACK"
    assert frame.payload["sequence"] == 12
