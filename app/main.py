# app/main.py
from app import create_app  # absolute import from app package

# Create the Flask app using the factory
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
