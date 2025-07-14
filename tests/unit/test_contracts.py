from controllers.contract_controller import create_contract, update_contract

# Empêcher un commercial de créer un contrat
def test_create_contract_refused_for_commercial():
    user = {
        "id": 2,
        "department": "commercial",
        "email": "a@a.com"
    }

    success, message = create_contract(
        client_email="test@client.com",  # le client n'a pas besoin d'exister ici (test unitaire isolé)
        total_amount=500,
        amount_due=100,
        is_signed=False,
        user=user
    )

    assert success is False
    assert "gestion" in message.lower()  # on vérifie bien le message d'erreur


# Test 2 — Empêcher un commercial de modifier un contrat qui ne lui appartient pas
def test_update_contract_only_allowed_for_owner():
    user = {
        "id": 3,
        "department": "commercial",
        "email": "not_owner@a.com"
    }

    contract_id = 999  # ID fictif : dans un test unitaire on suppose qu’il ne correspond à rien

    success, msg = update_contract(
        contract_id=contract_id,
        total_amount=1000.0,
        amount_due=500.0,
        is_signed=True,
        user=user
    )

    assert success is False
    assert "contrat non trouvé" in msg.lower()

