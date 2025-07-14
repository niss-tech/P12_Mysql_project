from menu import menu
from config.logging_config import init_sentry

init_sentry()


if __name__ == "__main__":
    # Lancer la vue CLI
    menu()