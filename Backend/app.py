from app import create_app

app = create_app() #se importa desde app/__init__ donde se configura la app

if __name__ == "__main__":
    app.run(debug=True)