import os
from main import create_app, db
from main.models import UserModel

app = create_app()
app.app_context().push()

if __name__ == "__main__":
    db.create_all()
    app.run(debug = True, host="0.0.0.0", port = 6000)