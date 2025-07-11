from controllers.user_controller import update_user

def update_user_cli():
    print("=== Modification d’un utilisateur ===")
    user_id = input("ID de l’utilisateur à modifier : ")

    new_first_name = input("Nouveau prénom (laisser vide pour ne pas changer) : ")
    new_last_name = input("Nouveau nom (laisser vide pour ne pas changer) : ")
    new_email = input("Nouvel email (laisser vide pour ne pas changer) : ")
    new_department = input("Nouveau département (gestion / commercial / support) : ")

    success, message = update_user(
        user_id,
        new_first_name or None,
        new_last_name or None,
        new_email or None,
        new_department or None
    )

    print(f"\n{'' if success else ''} {message}")
