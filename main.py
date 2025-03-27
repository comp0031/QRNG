import os
from entropy import METHODS, measure_time, scalability
from extraction_seeded.SeededExtractors import SeededExtractors

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
        "Generated": generated_path,
        "Extracted": extracted_path,
    }
    # iterate through categories and files
    bit_efficiency = {}
    generated_bits = {}
    for category, category_path in data.items():

        file_paths = [os.path.join(category_path, file_name) for file_name in os.listdir(category_path)]
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

        with open(output_path, "a") as f:
            f.write(f"\n======= {category} ========\n")

        file_paths = [os.path.join(category_path, file_name) for file_name in os.listdir(category_path)]
        if category == "Generated":
            methods = ["circulant", "dodis", "toeplitz", "trevisan"]
            seeded_extractor = SeededExtractors(file_paths, methods)
        # calculate metrics for each file
        for file_path in file_paths:
            file_name = os.path.basename(file_path)
            output_str = f"{file_name} => "
            for entropy_name, _ in METHODS.items():
                if entropy_name == "min_entropy" and category == "Generated":
                    H, t = measure_time(file_path, entropy_name, METHODS)
                    seeded_extractor.adjust_entropies(file_name, H)
                if entropy_name == "chsh":
                    chsh1_est, chsh2_est = get_chsh_estimates()
                    H, t = measure_time(file_path, entropy_name, METHODS, chsh1_est, chsh2_est)
                else:
                    H, t = measure_time(file_path, entropy_name, METHODS)
                output_str += f"{entropy_name}: {H:.6f} (time: {t:.4f}s), "

            print(output_str)
            with open(output_path, "a") as f:
                f.write(output_str + "\n")
        if category == "Generated":
            seeded_extractor.extract_randomness()
            seeded_extractor.write_output(extracted_path)

        # =========== efficiency final output =============
        
        for file_path in file_paths:
        # Count bits
            file_name = os.path.basename(file_path)
            
            # Determine number of bits (using file size for .bin files)
            if file_path.endswith(".bin"):
                num_bits = os.path.getsize(file_path)
            else:
                with open(file_path, "r") as f:
                    num_bits = len(f.read())
            
            if category == "Generated":
                # For a generated file, use the base name (without ".bin") as key for the generated_bits dict.
                base_key = file_name.removesuffix(".bin")
                generated_bits[base_key] = num_bits
                
                # Also store the generated file in bit_efficiency using the full file name.
                if file_name not in bit_efficiency:
                    bit_efficiency[file_name] = [0, 0, 0, 0]
                bit_efficiency[file_name][0] = num_bits

            else:  # category == "Extracted"
                # Expecting filenames like: "10M_TRI_DIQRNG_extracted_using_toeplitz.bin"
                if "_extracted_using_" in file_name:
                    left, right = file_name.split("_extracted_using_")
                    # Use the left part as the base name.
                    base_key = left  # e.g. "10M_TRI_DIQRNG"
                    method_name = right.removesuffix(".bin")  # e.g. "toeplitz"
                    # Build a new key that combines the generated file name and the method.
                    new_key = f"{base_key}.bin__{method_name}"
                else:
                    # Fallback if the expected pattern isn't found.
                    base_key = file_name.removesuffix(".bin")
                    new_key = file_name
                
                # Look up the generated bit count from our global dictionary.
                gen_val = generated_bits.get(base_key, 0)
                
                # Create or update the extracted file's entry in bit_efficiency.
                if new_key not in bit_efficiency:
                    bit_efficiency[new_key] = [0, 0, 0, 0]
                # Set the generated (inp_num) from the corresponding generated file.
                bit_efficiency[new_key][0] = gen_val
                # Set the extracted (out_num) value.
                bit_efficiency[new_key][1] = num_bits
                
                # If we have a nonzero generated value, compute the difference and percent.
                if gen_val != 0:
                    diff = gen_val - num_bits
                    bit_efficiency[new_key][2] = diff
                    bit_efficiency[new_key][3] = diff / gen_val * 100

        with open(output_path, "a") as f:
            f.write(f"\n======= Efficiency ========\n")
            for key, val in bit_efficiency.items():
                f.write(f"{key}: inp_num = {val[0]}, out_num = {val[1]}, diff = {val[2]}, % = {val[3]}\n")   

        # compute scalability for this category
        # with open(output_path, "a") as f:
        #     f.write(f"\n======= {category} Scalability ========\n")
        #     # sort file_paths by size for better regression
        #     file_paths.sort(key=lambda x: os.path.getsize(x))
        #     for entropy_name in METHODS:
        #         if entropy_name != "chsh":  # CHSH doesn't depend on file size
        #             slope, intercept = scalability(file_paths, entropy_name, METHODS)
        #             f.write(f"{entropy_name}: slope={slope:.4f}, intercept={intercept:.4f}\n")
        #             print(f"{entropy_name}: slope={slope:.4f}, intercept={intercept:.4f}")
        #         else:
        #             f.write(f"{entropy_name}: slope=N/A (fixed input)\n")
        #             print(f"{entropy_name}: slope=N/A (fixed input)")

if __name__ == "__main__":
    main()