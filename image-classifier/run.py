from classifier import app as application
from classifier import config

application.config.from_object(config)    
application.config.from_pyfile('config/config.py')

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=8000)
