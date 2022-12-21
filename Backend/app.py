from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
# import threading


# Start app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


# Custom endpoint
endpoint = '/api/v1'

# SOCKET.IO EVENTS


@socketio.on('connect')
def initial_connection():
    print('a new client connnect')


@app.route(endpoint + '/top/', methods=['GET'])
def get_allLikes():
    if request.method == 'GET':
        s = DataRepository.readAllLikes()
        return jsonify(s), 200


@socketio.on('F2B_get_likes')
def getLikes(jsonObject):
    print(jsonObject)
    isbn_nr = jsonObject['isbn_nr']
    title = jsonObject['name']
    cat = jsonObject['categorie']
    insert = DataRepository.readLikes(isbn_nr, title, cat)
    if insert:
        socketio.emit('B2F_showLikes', insert)

@socketio.on('F2B_update_likes')
def getLikes(jsonObject):
    title = jsonObject['bookName']
    insert = DataRepository.readUpdatedLikes(title)
    if insert:
        socketio.emit('B2F_showLikes', insert)


@socketio.on('F2B_add_like')
def updateLikes(jsonObject):
    bookName = jsonObject['bookName']
    print(bookName)
    data = DataRepository.updateLike(bookName)
    print(data)
    if data > 0:
        return jsonify(response="Likes van {0} aangepast ".format(bookName)), 200
    else:
        return jsonify(error="Isbn {} niet gevonden".format(bookName)), 404


@socketio.on('F2B_add_dislike')
def updateDislikes(jsonObject):
    bookName = jsonObject['bookName']
    data = DataRepository.updateDislike(bookName)
    print(data)
    if data > 0:
        return jsonify(response="Dislikes van {0} aangepast ".format(bookName)), 200
    else:
        return jsonify(error="Isbn {} niet gevonden".format(bookName)), 404




# Start app
if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=5500, debug=True)
    socketio.run(app, host='0.0.0.0', debug=True)
