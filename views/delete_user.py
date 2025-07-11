from controllers.user_controller import delete_user

def delete_user_cli():
    print("=== Suppression d’un utilisateur ===")
    user_id = input("ID de l’utilisateur à supprimer : ")
    confirmation = input("Confirmer la suppression ? (o/n) : ").lower()

    if confirmation != "o":
        print("Annulé.")
        return

    success, message = delete_user(user_id)
    print(f"\n{'' if success else ''} {message}")
