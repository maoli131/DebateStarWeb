# This file is the main entry (running) point for Debatestar web
import os
from debatestar import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)