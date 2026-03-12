import os
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        "service": "Cloud Run Demo-v2",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/image')
def show_image():
    return """
    <html>
      <head><title>Cloud Storage Image</title></head>
      <body>
        <h2>Image from Cloud Storage</h2>
        <img src="https://storage.googleapis.com/cloudrun_bucket22/pexels-ahmetyuksek-34123173.jpg" width="600">
      </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
