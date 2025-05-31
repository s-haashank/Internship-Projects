import pikepdf
import sys

def protect_pdf(input_pdf, output_pdf, password):
    try:
        # Open the original PDF
        pdf = pikepdf.open(input_pdf)

        # Save with encryption
        pdf.save(
            output_pdf,
            encryption=pikepdf.Encryption(owner=password, user=password, R=4)
        )

        print(f"✅ Password-protected PDF saved as {output_pdf}")

    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python another.py <input_pdf> <output_pdf> <password>")
        sys.exit(1)

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    password = sys.argv[3]

    protect_pdf(input_pdf, output_pdf, password)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 4:
        sys.argv = ['another.py', 'sample.pdf', 'protected_sample.pdf', 'secure123']
    main()
