from flask import Flask

def create_app():
    app = Flask(__name__) # crea una instancia de flask
    
    
    from .routes.routes import main
    app.register_blueprint(main) 
    
    return app