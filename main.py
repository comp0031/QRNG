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

    bit_efficiency = {}

    # iterate through categories and files
    for category, category_path in data.items():
        with open(output_path, "a") as f:
            f.write(f"\n======= {category} ========\n")

        file_paths = [os.path.join(category_path, file_name) for file_name in os.listdir(category_path)]

        # === efficiency start === 
        for file_path in file_paths:
            file_name = os.path.basename(file_path)

            # num bits extracted, num bits generated
            if file_path.endswith(".bin"):
                num_bits = os.path.getsize(file_path)
            else:
                with open(file_path, "r") as f:
                    num_bits = len(f.read())

            if file_name not in bit_efficiency:
                bit_efficiency[file_name] = [0, 0, 0, 0]  # [generated, extracted]

            if category == "Generated":
                bit_efficiency[file_name][0] = num_bits  # update generated
            else:
                bit_efficiency[file_name][1] = num_bits  # update extracted

            pre = bit_efficiency[file_name][0]
            post = bit_efficiency[file_name][1]
            if pre != 0 and post != 0:
                diff = pre - post
                bit_efficiency[file_name][2] = diff

                percent = diff / pre * 100
                bit_efficiency[file_name][3] = percent

            # === efficiency end === 

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

        # === efficiency start === 
        with open(output_path, "a") as f:
            f.write(f"\n======= Efficiency ========\n")
            for key, val in bit_efficiency.items():
                f.write(f"{key}: inp_num = {val[0]}, out_num = {val[1]}, diff = {val[2]}, percent = {val[3]}\n")                
        # === efficiency end === 

if __name__ == "__main__":
    main()