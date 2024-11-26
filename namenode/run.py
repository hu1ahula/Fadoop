from app import create_app
import threading

app = create_app()


if __name__ == '__main__':
    app.run(debug=True, port=8001)