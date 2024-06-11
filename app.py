from flask import Flask, jsonify
from model.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'message': 'Server is healthy'})

if __name__ == '__main__':
    app.run(debug=True)