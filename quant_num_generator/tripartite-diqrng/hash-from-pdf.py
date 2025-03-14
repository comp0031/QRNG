import hashlib


def hash_pdf_to_number(pdf_path):
    # Read the file in binary mode
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    # Compute SHA-256 hash
    hash_digest = hashlib.sha256(pdf_content).hexdigest()

    # Convert hash to a large integer
    hash_number = int(hash_digest, 16)

    return hash_number


# Example usage
pdf_path = "pdfcoffee.com-emily-remler copy.pdf"  # Replace with your file
random_number = bin(hash_pdf_to_number(pdf_path))
