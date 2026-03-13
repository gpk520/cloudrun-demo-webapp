import os
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template_string
from google.cloud import storage

app = Flask(__name__)

# Initialize the Cloud Storage client (uses the default service account)
storage_client = storage.Client()

def generate_signed_url(bucket_name, blob_name, expiration=3600):
    """Generate a v4 signed URL for downloading a blob."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(seconds=expiration),
        method="GET",
    )
    return url

@app.route('/')
def index():
    """Return a simple JSON response with the service name and timestamp."""
    return jsonify({
        "service": "Cloud Run Demo-v4",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/image')
def show_image():
    """Display an HTML page with the image fetched via a signed URL."""
    # Generate a signed URL valid for 1 hour (3600 seconds)
    image_url = generate_signed_url(
        bucket_name='cloudrun_bucket22',
        blob_name='pexels-ahmetyuksek-34123173.jpg',
        expiration=3600
    )

    # Embed the signed URL in an <img> tag
    html = f'''
    <!DOCTYPE html>
    <html>
      <head>
        <title>Cloud Storage Image</title>
      </head>
      <body>
        <h2>Image from Cloud Storage (private bucket, signed URL)</h2>
        <img src="{image_url}" alt="Demo Image" style="max-width: 600px;">
        <p><small>This URL expires in 1 hour.</small></p>
      </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
