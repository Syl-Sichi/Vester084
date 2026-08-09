from zelda.mobile.journal import MobileEventJournal
from zelda.mobile.transport import TransportFrame


def test_journal_survives_reopen(tmp_path):
    path = str(tmp_path / "mobile.db")
    journal = MobileEventJournal(path, max_items=10)
    event = journal.append(TransportFrame("EVENT", payload={"message": "hello"}))
    journal.close()

    reopened = MobileEventJournal(path, max_items=10)
    replay = reopened.after(0)
    reopened.close()

    assert replay[0].sequence == event.sequence
    assert replay[0].frame.payload == {"message": "hello"}
