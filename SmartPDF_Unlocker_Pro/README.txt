SmartPDF Unlocker Pro


A powerful Python-based command-line tool that unlocks password-protected PDF files using a wordlist attack. Designed as part of an internship project, this tool demonstrates real-world cybersecurity concepts and PDF encryption handling using the `pikepdf` library.


HOW TO SET UP
--------------------
1. Make sure Python 3.x is installed on your system.

2. Install dependencies using:
   pip install -r requirements.txt

3. This folder contains:
   - main.py                 : The main script
   - wordlist.txt            : List of possible passwords
   - samples/sample.pdf      : Locked input PDF
   - samples/unlocked_output.pdf : Output after cracking

--------------------
HOW TO USE
--------------------
Run the script using:

   python main.py

If the correct password is found (e.g., "2005"), the PDF will be unlocked and saved as `samples/unlocked_output.pdf`.

--------------------
FEATURES
--------------------
- Brute-force PDF password cracker using a wordlist
- Secure and fast decryption using `pikepdf`
- Real-time progress bar via `tqdm`
- Organized output and modular folder structure

--------------------
DEMO PASSWORD
--------------------
- The sample PDF included is locked with the password: **2005**
- Make sure "2005" is included in `wordlist.txt`
