from bot import run_bot
from translation import set_language


def main():
    print("App started!")
    set_language('ua')
    # connect_to_db()
    run_bot()


if __name__ == "__main__":
    main()
