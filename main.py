import os
from entropy import METHODS

def get_chsh_estimates():
    """
    Function to retrieve CHSH1 and CHSH2 estimates from a data source.
    """
    # TODO: Implement proper retrieval of CHSH values
    chsh1_est, chsh2_est = 2.5, 2.6  # placeholder vals for now
    return chsh1_est, chsh2_est


def main() -> None:
    output_path = os.path.join("output", "outputs.txt")
    # clear the output file
    with open(output_path, "w") as f:
        f.write("")

    # get all the input files in the extracted directory
    extracted_path = os.path.join("inp", "extracted")
    generated_path = os.path.join("inp", "generated")

    data = {
        "Extracted": extracted_path,
        "Generated": generated_path,
    }

    # iterate through the different categories and the files in their folders
    for category, category_path in data.items():
        with open(output_path, "a") as f:
            f.write(f"\n======= {category} ========\n")

        for file_name in os.listdir(category_path):
            # create the absolute file path to the file
            file_path = os.path.join(category_path, file_name)

            # calculate entropy over all the entropy methods
            output_str = f"{file_name} => "
            for entropy_name, entropy_func in METHODS.items():
                if entropy_name == "chsh":
                    chsh1_est, chsh2_est = get_chsh_estimates()
                    H = entropy_func(chsh1_est, chsh2_est)
                else:
                    H = entropy_func(file_path)
                output_str += f"{entropy_name}: {H:.4f}, "

            print(output_str)
            with open(output_path, "a") as f:
                f.write(output_str + "\n")
                

if __name__ == "__main__":
    main()
