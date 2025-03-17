import os
from entropy import METHODS, measure_time, scalability

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

    # get input files
    extracted_path = os.path.join("inp", "extracted")
    generated_path = os.path.join("inp", "generated")

    data = {
        "Extracted": extracted_path,
        "Generated": generated_path,
    }

    # iterate through categories and files
    for category, category_path in data.items():
        with open(output_path, "a") as f:
            f.write(f"\n======= {category} ========\n")

        file_paths = [os.path.join(category_path, file_name) for file_name in os.listdir(category_path)]

        # calculate metrics for each file
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            output_str = f"{file_name} => "
            for entropy_name, _ in METHODS.items():
                if entropy_name == "chsh":
                    chsh1_est, chsh2_est = get_chsh_estimates()
                    H, t = measure_time(file_path, entropy_name, METHODS, chsh1_est, chsh2_est)
                else:
                    H, t = measure_time(file_path, entropy_name, METHODS)
                output_str += f"{entropy_name}: {H:.6f} (time: {t:.4f}s), "

            print(output_str)
            with open(output_path, "a") as f:
                f.write(output_str + "\n")

        # compute scalability for this category
        with open(output_path, "a") as f:
            f.write(f"\n======= {category} Scalability ========\n")
            # sort file_paths by size for better regression
            file_paths.sort(key=lambda x: os.path.getsize(x))
            for entropy_name in METHODS:
                if entropy_name != "chsh":  # CHSH doesn't depend on file size
                    slope, intercept = scalability(file_paths, entropy_name, METHODS)
                    f.write(f"{entropy_name}: slope={slope:.4f}, intercept={intercept:.4f}\n")
                    print(f"{entropy_name}: slope={slope:.4f}, intercept={intercept:.4f}")
                else:
                    f.write(f"{entropy_name}: slope=N/A (fixed input)\n")
                    print(f"{entropy_name}: slope=N/A (fixed input)")

if __name__ == "__main__":
    main()