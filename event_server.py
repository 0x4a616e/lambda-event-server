import queue
import uuid

import flask

hostName = "localhost"
serverPort = 8082

requests = queue.Queue()
responses = queue.Queue()

app = flask.Flask(__name__)


@app.route("/invoke", methods=['POST'])
def invoke():
    requests.put(flask.request.get_data().decode('UTF-8'))
    return responses.get()


@app.route("/2018-06-01/runtime/invocation/next", methods=['GET'])
def next_event():
    event = requests.get()

    resp = flask.Response(str(event))
    resp.headers['Content-type'] = "text/plain"
    resp.headers['Lambda-Runtime-Aws-Request-Id'] = str(uuid.uuid4())
    resp.headers['Lambda-Runtime-Trace-Id'] = str(uuid.uuid4())
    return resp


@app.route("/2018-06-01/runtime/invocation/<request_id>/response", methods=['POST'])
def post_response(request_id):
    responses.put(flask.request.get_data().decode('UTF-8'))

    return flask.Response()


@app.route("/2018-06-01/runtime/invocation/<request_id>/error", methods=['POST'])
def post_error(request_id):
    responses.put(flask.request.get_data().decode('UTF-8'))

    return flask.Response()


if __name__ == '__main__':
    app.run(host=hostName, port=serverPort)
