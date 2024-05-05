from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# Try changing jsonify to make_response

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    if request.method =='GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at.asc()).all()]
        return make_response(messages)
    
    elif request.method == 'POST':
        new_message = Message(
            body=request.json.get("body"), 
            username=request.json.get("username"), 
        )

        db.session.add(new_message)
        db.session.commit()

        print("New message:", new_message)  
        print("All messages:", Message.query.all()) 

        return make_response(new_message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response({'error': 'Message not found'}), 404

    if request.method == 'GET':
        return make_response(message.to_dict()), 200

    elif request.method == 'PATCH':
        body = request.json.get("body")  
        if body:
            message.body = body
            db.session.commit()
        return make_response(message.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return '', 204
