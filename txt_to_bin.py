with open("inp/python_random.txt") as file:
    bits = file.read()

output = []

for bit in bits:
    output.append(0 if bit == "0" else 1)

ba = bytearray(output)
bs = bytes(ba)

with open("inp/python_random.bin", "wb") as file:
    file.write(bs)
