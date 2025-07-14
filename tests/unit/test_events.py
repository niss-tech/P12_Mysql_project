from controllers.event_controller import update_event_by_support


def test_update_event_by_wrong_support():
    """Un support ne peut pas modifier un événement qui ne lui est pas assigné."""
    user_id = 123
    event_id = 999  # supposé ne pas appartenir à cet ID
    success, msg = update_event_by_support(user_id, event_id, {"location": "Nice"})
    assert success is False
    assert "introuvable" in msg.lower() or "non autorisé" in msg.lower()
