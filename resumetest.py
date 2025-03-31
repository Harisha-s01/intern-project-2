import imaplib
import email
import os
import re
from PyPDF2 import PdfReader
import mysql.connector

EMAIL = "harishasivakumar001@gmail.com"
PASSWORD = "xrwh sspv miud grpj"
IMAP_SERVER = "imap.gmail.com"
ALLOWED_EXTENSIONS = [".pdf", ".docx", ".doc"]

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Harisha#8"
DB_NAME = "haridb 1"

def is_resume(filename):
    nameFile, ext = os.path.splitext(filename)
    return (ext.lower() in ALLOWED_EXTENSIONS) and ("resume" in nameFile.lower())

def normalize_text(text):
    """ Convert multi-line PDF text into a single continuous string """
    text = ' '.join(text.splitlines()).replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)  
    return text

def extract_phone_and_email(text):
    phone_pattern = r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_numbers = re.findall(phone_pattern, text)
    emails = re.findall(email_pattern, text)
    return phone_numbers, emails

def extract_skills(text):
    skills_list = [
        "Python", "Java", "C++", "JavaScript", "SQL", "HTML", "CSS", "Machine Learning",
        "AWS", "Docker", "Kubernetes", "Data Science", "TensorFlow", "Power BI", "React"
    ]
    
    found_skills = [skill for skill in skills_list if skill.lower() in text.lower()]
    return ', '.join(found_skills) if found_skills else "Not found"

import re

def extract_education(text):
    """
    Extracts only the degree and college, handling multi-line and complex formats.
    """
    text = re.sub(r'\s+', ' ', text).strip()

    edu_pattern = re.compile(
                                         
      r"(?:^|\s)([A-Za-z\s.'’&-\(\)]{0,15}(?:College|University|Institute|School|Acad(?:emy)?)(?:\sof\s[A-Za-z\s.'’&-\(\)]{0,30})?)(?:\s|$)"  
        r".*?(Bachelor Of Engineering|Bachelor Of Technology|Master of Engineering|B\.Tech|B\.E\.|M\.Tech|MCA|BCA|MSc|BSc|Diploma)",  
        re.IGNORECASE
    )

    education_details = []

    for match in edu_pattern.findall(text):
        college, degree = match
        degree = degree.strip()
        college = college.strip()
        education_details.append(f"{college} - {degree}")

    return ', '.join(education_details) if education_details else "Not found"

def extract_certificates(text):
    cert_pattern = re.compile(
        r"(?:Certification|Certified|Certificate).*?(AWS|Azure|Python|Java|ML|AI|Cloud|Power BI|Data Science|DevOps|Web Designing)", 
        re.IGNORECASE
    )

    cert_matches = cert_pattern.findall(text)

    certificates = []
    for match in cert_matches:
        cert = match.strip()
        certificates.append(cert)

    return ', '.join(set(certificates)) if certificates else "Not found"

def download_resumes(mail):
    mail.select("inbox")
    status, messages = mail.search(None, "ALL")
    email_ids = messages[0].split()[-10:]  
    email_ids.reverse()  

    downloaded_files = []
    for email_id in email_ids:
        try:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_disposition() == "attachment":
                                filename = part.get_filename()
                                if filename and is_resume(filename):
                                    if not os.path.exists("downloads"):
                                        os.makedirs("downloads")
                                    filepath = os.path.join("downloads", filename)
                                    with open(filepath, "wb") as f:
                                        f.write(part.get_payload(decode=True))
                                    downloaded_files.append(filepath)
        except Exception as e:
            print(f"Error processing email ID {email_id.decode()}: {e}")
    return downloaded_files

def process_resumes_and_insert_to_db(file_paths):
    try:
        db = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor = db.cursor()

        for file_path in file_paths:
            try:
                print(f"Processing file: {file_path}")
                
                
                reader = PdfReader(file_path)
                resume_content = ""
                for page in reader.pages:
                    resume_content += page.extract_text() or ""
                   
                normalized_text = normalize_text(resume_content)   
                
                phone_numbers, emails = extract_phone_and_email(normalized_text)
                skills = extract_skills(normalized_text)
                education = extract_education(normalized_text)
                certificates = extract_certificates(normalized_text)

            
                for phone in phone_numbers:
                    for email in emails:
                        sql = """
                        INSERT INTO resumetest (phonenumber, email, skills, education, certificates)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        values = (phone, email, skills, education, certificates)
                        cursor.execute(sql, values)
                
                db.commit()
                print(f"Inserted data from {file_path} into database.")

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

        cursor.close()
        db.close()
        print("Database connection closed.")
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")

if __name__ == "__main__":
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, timeout=10)
        mail.login(EMAIL, PASSWORD)
        print("Logged in to email successfully.\n")

        downloaded_files = download_resumes(mail)
        if not downloaded_files:
            print("No resumes found.")
        else:
            print(f"Downloaded {len(downloaded_files)} resumes.")

            process_resumes_and_insert_to_db(downloaded_files)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        mail.logout()
        print("Logged out from email.")
