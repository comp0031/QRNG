import os
from entropy import METHODS



def main() -> None:
    output_path = os.path.join("output", "outputs.txt")
    # clear the output file
    with open(output_path, "w") as f:
        f.write("")
    # get all the input files in the inp directory
    for file_name in os.listdir("inp"): 
        # create the absolute file path to the file
        file_path = os.path.join("inp", file_name)

        # calculate entropy over all the entropy methods


        output_str = f"File: {file_name}, "
        for entropy_name, entropy_func in METHODS.items():
            H = entropy_func(file_path)
            output_str += f"{entropy_name} => {H:.5f}, "
            print(output_str)
            with open(output_path, "a") as f:
                f.write(output_str + "\n")

if __name__ == "__main__":
    main()
