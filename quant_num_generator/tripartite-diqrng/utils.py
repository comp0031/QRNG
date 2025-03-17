import hashlib
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Convert hash of pdf to binary sequence for generation or checking round selection
# Use HKDF to extent the hash for longer sequences.
# Takes pdf path and desired output length as parameters.


def hash_pdf_to_number(pdf_path: str, desired_len: int) -> str:
    with open(pdf_path, "rb") as f:
        pdf_content = f.read()

    hash_value = hashlib.sha256(pdf_content).digest()

    hkdf = HKDF(
        algorithm=hashes.SHA512(),
        length=desired_len//8,
        salt=None,
        info=b"pdf-expansion",
        backend=default_backend(),
    )

    expanded_seq = hkdf.derive(hash_value)

    
    binary_string = "".join(format(byte, "08b") for byte in expanded_seq)

    print(len(binary_string))

    return binary_string


#testing
#pdf_path = "quant_num_generator/tripartite-diqrng/pdfcoffee.com-emily-remler copy.pdf"
#hash_pdf_to_number(pdf_path,1024)
