import os
from entropy import METHODS



def main() -> None:
    # get all the input files in the inp directory
    for file_name in os.listdir("inp"): 
        # create the absolute file path to the file
        file_path = os.path.join("inp", file_name)

        # calculate entropy over all the entropy methods
        for entropy_name, entropy_func in METHODS.items():
            H = entropy_func(file_path)
            print(f"Method: {entropy_name}, Entropy: {H:.4f} bits")

if __name__ == "__main__":
    main()
