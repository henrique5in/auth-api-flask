from flask import Flask, jsonify, request
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from model.user import User
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'message': 'Server is healthy'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            print(current_user.is_authenticated)
            return jsonify({'message': 'Login success'})
    return jsonify({'message': 'username or password is incorrect'}), 400

@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout success'})

@app.route('/api/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Create user success'}), 201
    return jsonify({'message': 'invalid credentials'}), 400

@app.route('/api/user', methods=['GET'])
@login_required
def get_all_user():
    users = User.query.all()
    users = [{'id': user.id, 'username': user.username} for user in users]
    return jsonify(users)

@app.route('/api/user/<int:id_user>', methods=['GET'])
@login_required
def get_user(id_user):
    user = User.query.get(id_user)
    if user:
        return jsonify({'username': user.username})
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/user/<int:id_user>', methods=['PUT'])
@login_required
def update_user(id_user):
    data = request.json
    user = User.query.get(id_user)
    if user and data.get('password'):
        password = data.get('password')
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': f'user {id_user} updated successfully'})
    return jsonify({'message': 'User not found'}), 404

@app.route('/api/user/<int:id_user>', methods=['DELETE'])
@login_required
def delete_user(id_user):
    user = User.query.get(id_user)
    if current_user.id == id_user:
            return jsonify({'message': 'You cannot delete your own account'}), 400
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'user {id_user} deleted successfully'})
    return jsonify({'message': 'User not found'}), 404
    

if __name__ == '__main__':
    app.run(debug=True)