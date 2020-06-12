
from recording_rest_api import api
from recording_rest_api import app

if __name__ == "__main__":
    api.initialize_app()
    #    app.run(host='0.0.0.0', ssl_context=('cert/cert.pem', 'cert/key.pem'))
    app.run(host='0.0.0.0')
