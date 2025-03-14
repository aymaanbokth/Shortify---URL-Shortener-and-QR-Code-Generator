from flask import Flask, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import shortuuid
import qrcode
import re  # ✅ Import regex for validation
from datetime import datetime

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS to allow frontend access

# Database configuration (Use PostgreSQL for deployment)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/shortify")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Define the ShortURL model
class ShortURL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    qr_code = db.Column(db.String(500), nullable=True)  # Path to QR code image
    clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime, nullable=True)  # Track last click timestamp
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Initialize the database
with app.app_context():
    db.create_all()

# Function to generate a unique short code
def generate_short_code():
    return shortuuid.ShortUUID().random(length=6)  # ✅ 6-character short code

# Function to validate a custom short code
def is_valid_short_code(code):
    return bool(re.match("^[a-zA-Z0-9]+$", code))  # ✅ Allow only letters and numbers

# Function to generate a QR code
def generate_qr_code(short_url):
    qr = qrcode.make(short_url)
    qr_folder = os.path.join(os.getcwd(), "static", "qr")
    os.makedirs(qr_folder, exist_ok=True)

    qr_filename = f"{short_url.split('/')[-1]}.png"
    qr_path = os.path.join(qr_folder, qr_filename)
    qr.save(qr_path)

    return f"/static/qr/{qr_filename}"  # ✅ Relative path for Flask API

# Route to shorten a URL (with QR code)
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    original_url = data.get("url")
    custom_code = data.get("custom_code")

    if not original_url:
        return jsonify({"error": "URL is required"}), 400

    # Validate URL format
    if not re.match(r"^(https?://)", original_url):
        return jsonify({"error": "Invalid URL format. Must start with http:// or https://"}), 400

    # Validate custom code (if provided)
    if custom_code:
        if not is_valid_short_code(custom_code):
            return jsonify({"error": "Custom short code must be alphanumeric (A-Z, a-z, 0-9) with no spaces"}), 400

        existing_url = ShortURL.query.filter_by(short_code=custom_code).first()
        if existing_url:
            return jsonify({"error": "Custom short code is already taken"}), 400
        short_code = custom_code  
    else:
        short_code = generate_short_code()

    short_url = f"{request.host_url}{short_code}"  # ✅ Uses dynamic host URL

    # Generate QR Code
    qr_code_path = generate_qr_code(short_url)

    # Store in database
    new_short_url = ShortURL(original_url=original_url, short_code=short_code, qr_code=qr_code_path)
    db.session.add(new_short_url)
    db.session.commit()

    return jsonify({
        "original_url": original_url,
        "short_url": short_url,
        "qr_code": f"{request.host_url}{qr_code_path}"  # ✅ Uses full URL for QR code
    })

# Route to redirect a short URL to the original URL & track clicks
@app.route('/<short_code>')
def redirect_to_url(short_code):
    short_url = ShortURL.query.filter_by(short_code=short_code).first()

    if short_url:
        short_url.clicks += 1
        short_url.last_clicked = datetime.utcnow()
        db.session.commit()
        return redirect(short_url.original_url)

    return jsonify({"error": "Short URL not found"}), 404

# Route to get analytics for a short URL
@app.route('/analytics/<short_code>', methods=['GET'])
def get_analytics(short_code):
    short_url = ShortURL.query.filter_by(short_code=short_code).first()

    if not short_url:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "original_url": short_url.original_url,
        "short_url": f"{request.host_url}{short_url.short_code}",
        "clicks": short_url.clicks,
        "created_at": short_url.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "last_clicked": short_url.last_clicked.strftime("%Y-%m-%d %H:%M:%S") if short_url.last_clicked else "Never clicked"
    })

if __name__ == '__main__':
    app.run(debug=True)
