from main import create_app
import os


app = create_app()
app.app_context().push()

if __name__ == "__main__":
    app.run(debug = True, port = 6000)
