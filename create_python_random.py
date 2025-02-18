import random


# bits = ''.join(random.choice("01") for _ in range(10000))
# # Write the bit string to a text file.
# with open("inp/python_random.txt", "w") as f:
#     f.write(bits)


bits = ''.join(random.choices("01", weights=[5,1], k=10000))
# Write the bit string to a text file.
with open("python_not_random.txt", "w") as f:
    f.write(bits)