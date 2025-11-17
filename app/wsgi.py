import sys
import traceback
from app import create_app

try:
    app = create_app()
except Exception:
    # Print traceback to stdout so Render captures the error in logs, then exit
    traceback.print_exc()
    sys.exit(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
