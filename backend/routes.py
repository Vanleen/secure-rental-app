from flask import request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app, db
from models import User, Document
from utils import verify_document, extract_metadata, create_onfido_applicant, upload_document_to_onfido, send_verification_email

def init_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/upload', methods=['GET', 'POST'])
    @jwt_required()
    def upload_document():
        if request.method == 'POST':
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            document_type = request.form['document_type']
            document_file = request.files['document_file']
            document_path = f'uploads/{document_file.filename}'
            document_file.save(document_path)

            # Créer un applicant Onfido
            onfido_applicant = create_onfido_applicant(user.username, user.username, user.email)
            applicant_id = onfido_applicant['id']

            # Télécharger le document vers Onfido
            onfido_response = upload_document_to_onfido(applicant_id, document_path, document_type)
            is_verified = onfido_response.get('status') == 'complete'

            document = Document(user_id=user_id, document_type=document_type, document_path=document_path, is_verified=is_verified)
            db.session.add(document)
            db.session.commit()

            # Envoyer un email de notification
            send_verification_email(user.email, document_type, is_verified)

            return redirect(url_for('dashboard'))

        return render_template('upload.html')

    @app.route('/dashboard')
    @jwt_required()
    def dashboard():
        user_id = get_jwt_identity()
        documents = Document.query.filter_by(user_id=user_id).all()
        return render_template('dashboard.html', documents=documents)

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        username = data['username']
        email = data['email']
        password = data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return jsonify(access_token=access_token), 200
        return jsonify({'message': 'Invalid credentials'}), 401

    @app.route('/check-status', methods=['GET'])
    @jwt_required()
    def check_status():
        user_id = get_jwt_identity()
        documents = Document.query.filter_by(user_id=user_id).all()
        response = {
            'documents': [{'id': doc.id, 'is_verified': doc.is_verified} for doc in documents]
        }
        return jsonify(response)
