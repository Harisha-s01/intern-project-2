# Resume Data Extraction from Gmail to SQL Workbench

## Overview

This project automates the process of extracting data from resume files attached to emails in a Gmail inbox and storing this information in a SQL Workbench database. It leverages Python's `imaplib` for accessing Gmail, `email` for parsing email content, and a suitable library (e.g., `pdfminer.six`, `docx2txt`, `textract`) for extracting text from various resume file formats. The extracted data is then inserted into a pre-defined table in your SQL Workbench database using a Python database connector (e.g., `mysql.connector`, `psycopg2`, `pyodbc`).

## Features

* **Gmail Integration:** Connects to your Gmail account using IMAP to fetch emails.
* **Attachment Filtering:** Identifies and downloads resume files based on configurable file extensions (e.g., `.pdf`, `.docx`).
* **Content Extraction:** Extracts text content from downloaded resume files.
* **Data Parsing (Basic):** Includes basic regular expressions to extract key information like:
    * Email
    * Phone Number
    * College Name and degree (using a configurable regex)
    * Certificates ( keyword matching)
    * Skills ( keyword matching)
* **SQL Database Integration:** Connects to your SQL Workbench database and inserts the extracted data into a specified table.
* **Configuration:** Allows users to configure Gmail credentials, IMAP server details, database connection parameters, target mailbox, and file extensions to process.
* **Error Handling:** Includes basic error handling for network issues, file processing errors, and database connection problems.
