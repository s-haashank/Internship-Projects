import os
import PyPDF2

# File paths
sample_pdf_path = "samples/sample.pdf"
wordlist_path = "wordlist.txt"
unlocked_pdf_path = "unlocked/unlocked_sample.pdf"
log_file = "logs.txt"

# Ensure the sample PDF exists
if not os.path.exists(sample_pdf_path):
    print(f"Error: {sample_pdf_path} not found.")
    exit()

# Ensure wordlist exists
if not os.path.exists(wordlist_path):
    print(f"Error: {wordlist_path} not found.")
    exit()

# Try passwords from wordlist
with open(wordlist_path, "r") as wordlist:
    passwords = [line.strip() for line in wordlist]

    for password in passwords:
        try:
            with open(sample_pdf_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)

                if reader.is_encrypted:
                    reader.decrypt(password)

                # Try reading a page
                reader.pages[0]

                # If success, unlock and save
                writer = PyPDF2.PdfWriter()
                for page in reader.pages:
                    writer.add_page(page)

                with open(unlocked_pdf_path, "wb") as output:
                    writer.write(output)

                print(f"[SUCCESS] Password found: {password}")
                with open(log_file, "a") as log:
                    log.write(f"Password found: {password}\n")
                break

        except Exception as e:
            continue
    else:
        print("[FAILED] No password matched.")
        with open(log_file, "a") as log:
            log.write("Password not found.\n")
