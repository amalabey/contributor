import sys
from platform_integration.webhook import app
from dotenv import load_dotenv


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) > 0 and args[0] == "serve":
        load_dotenv(".env")
        app.run()
    else:
        print("Invalid command.")
