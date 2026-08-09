from zelda.control.write_policy import WriteAuthorization, require_write_authorization


def test_write_requires_explicit_confirmation():
    try:
        require_write_authorization("workspace.note.write", None)
    except PermissionError as exc:
        assert str(exc) == "write_confirmation_required"
    else:
        raise AssertionError("expected write_confirmation_required")


def test_write_authorization_must_match_capability():
    auth = WriteAuthorization("workspace.other.write", True)
    try:
        require_write_authorization("workspace.note.write", auth)
    except PermissionError as exc:
        assert str(exc) == "write_authorization_mismatch"
    else:
        raise AssertionError("expected write_authorization_mismatch")


def test_confirmed_matching_authorization_is_accepted():
    auth = WriteAuthorization("workspace.note.write", True)
    require_write_authorization("workspace.note.write", auth)
