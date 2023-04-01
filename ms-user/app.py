from main import create_app
import os
from main.utils import exist_database
from main import db

app = create_app()
app.app_context().push()
cursor = db.cursor()

if __name__ == "__main__":
    exist_database(cursor)
    app.run(debug = True, host="0.0.0.0", port = 6000)
    