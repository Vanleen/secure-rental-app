import requests
from app import app, mail
from flask_mail import Message
import hashlib

def create_onfido_applicant(first_name, last_name, email):
    url = f"{app.config['ONFIDO_API_URL']}/applicants"
    headers = {
        'Authorization': f"Token token={app.config['ONFIDO_API_KEY']}",
        'Content-Type': 'application/json'
    }
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def upload_document_to_onfido(applicant_id, document_path, document_type):
    url = f"{app.config['ONFIDO_API_URL']}/documents"
    headers = {
        'Authorization': f"Token token={app.config['ONFIDO_API_KEY']}",
    }
    files = {
        'file': open(document_path, 'rb'),
        'type': (None, document_type)
    }
    data = {
        'applicant_id': applicant_id
    }
    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()

def send_verification_email(user_email, document_type, is_verified):
    subject = "Document Verification Status"
    if is_verified:
        body = f"Dear user, your {document_type} has been verified successfully."
    else:
        body = f"Dear user, your {document_type} could not be verified. Please upload a valid document."

    msg = Message(subject, recipients=[user_email])
    msg.body = body
    mail.send(msg)

def extract_metadata(file_path):
    import PyPDF2
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        metadata = reader.getDocumentInfo()
    return metadata

def verify_document(document_type, metadata):
    if document_type == 'payslip':
        return verify_payslip(metadata)
    elif document_type == 'tax_notice':
        return verify_tax_notice(metadata)
    elif document_type == 'id_card':
        return verify_id_card(metadata)
    return False

def verify_payslip(metadata):
    return metadata.get('/Author') == 'Entreprise X'

def verify_tax_notice(metadata):
    return metadata.get('/Producer') == 'PDF Producer Z'

def verify_id_card(metadata):
    return metadata.get('/Creator') == 'Government ID Issuer'

def hash_content(content):
    sha256 = hashlib.sha256()
    sha256.update(content.encode('utf-8'))
    return sha256.hexdigest()
