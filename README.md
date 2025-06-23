**Resume Data Extraction from Gmail to SQL Workbench**

**Overview**  
This project automates the task of downloading resume files from a Gmail inbox, extracting important details from them, and storing the data in a MySQL database (such as SQL Workbench).  
The system connects to Gmail using IMAP, downloads attachments (such as PDF files), extracts text, parses key details (like phone number, email, education, skills, and certificates), and inserts the data into a database for easy access and analysis.



### How It Works

**Connect to Gmail**  
The script logs in to a Gmail account using IMAP (Internet Message Access Protocol) to access your inbox.

**Search for Emails**  
It searches for recent emails and looks for attachments that are likely to be resumes.

**Download Resume Files**  
Attachments with supported file types (e.g., PDF, DOCX, DOC) and names containing "resume" are downloaded to a local folder.

**Extract Text from Files**  
The script extracts text content from the resume files (currently supports PDF using PyPDF2).

**Parse Key Information**  
Using regular expressions and keyword matching, it extracts:  
- Phone numbers (10-digit or +91 format)  
- Email addresses  
- College names and degrees  
- Skills (from a predefined list)  
- Certificates (identified by common keywords)

**Store in Database**  
The extracted data is inserted into a MySQL database table for storage and later use.



### Features

- **Gmail integration:** Secure connection using IMAP to fetch emails.  
- **Attachment filtering:** Downloads only files that match allowed extensions (e.g., .pdf, .docx, .doc) and file-name patterns.  
- **Text extraction:** Extracts and normalizes text from PDF resumes (extensible to DOCX/DOC).  
- **Data parsing:** Extracts structured data (phone, email, education, skills, certificates).  
- **Database storage:** Inserts data into a MySQL database.  
- **Configurable settings:** Easily modify email, database, and file-type settings.  
- **Basic error handling:** Handles network, file, and database issues gracefully.



### Technologies

- Python 3.x  
- `imaplib`, `email` (email access)  
- `PyPDF2` (PDF text extraction)  
- `mysql-connector-python` (MySQL database access)  
- `re` (regular expressions for parsing)



### Example Database Table

- CREATE DATABASE resumes_db;
- USE resumes_db;

- CREATE TABLE resumetest (
  id INT AUTO_INCREMENT PRIMARY KEY,
  phonenumber VARCHAR(20),
  email VARCHAR(255),
  skills TEXT,
  education TEXT,
  certificates TEXT
);

### Requirements
**Install dependencies:**
pip install PyPDF2 mysql-connector-python

**Configuration**
Before running the script, configure these settings in your code:

- EMAIL = "your-email@gmail.com"
- PASSWORD = "your-app-password"  # Use an app password if 2FA is enabled
- IMAP_SERVER = "imap.gmail.com"

- DB_HOST = "localhost"
- DB_USER = "your-db-username"
- DB_PASSWORD = "your-db-password"
- DB_NAME = "resumes_db"

**Running the Project**
- Run the main script:
- python main.py
