from translation import set_language
from db import connect_to_db
from bot import run_bot

def main():
    set_language('ua')
    connect_to_db()
    run_bot()


if __name__ == "__main__":
    print("App started!")
    main()
