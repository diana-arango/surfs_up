# This dependancy will enable your code to access all that Flask has to offer.
from flask import Flask

# Create a new Flask app instance (singular version of something)
app = Flask(__name__)

# Create a root
@app.route('/')
def hello_world():
    return 'Hello world'

if __name__ == "__main__":
    app.run()
