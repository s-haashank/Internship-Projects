import pikepdf

# PDF numbers for check
pdf_numbers = [1, 2, 3]

# Wordlist
with open('wordlist.txt', 'r') as file:
    passwords = [line.strip() for line in file]

for num in pdf_numbers:
    pdf_path = f'samples/locked_sample({num}).pdf'
    output_path = f'samples/unlocked_sample({num}).pdf'

    print(f"\n[*] Trying to unlock: locked_sample({num}).pdf")

    for password in passwords:
        try:
            pdf = pikepdf.open(pdf_path, password=password)
            pdf.save(output_path)
            pdf.close()
            print(f"✅ Unlocked and saved as: unlocked_sample({num}).pdf")
            break
        except pikepdf.PasswordError:
            print(f"❌ Incorrect password: {password}")
        except FileNotFoundError:
            print(f"[ERROR] File not found: {pdf_path}")
            break
