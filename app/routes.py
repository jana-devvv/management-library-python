from app import app

@app.route('/')
def home():
    return 'Welcome to JD Management Library System by Jasen'