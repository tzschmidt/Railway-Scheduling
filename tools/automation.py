# automation.py
import subprocess
import sys
import os

def generate_output_filename(input_file, extension):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    return f"test/{base_name}_output.{extension}"

def process_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            input_pkl = os.path.join(directory, filename)

            # Generate the output file names based on the input file name
            output_lp = generate_output_filename(input_pkl, "lp")
            output_txt = generate_output_filename(input_pkl, "txt")

            # Convert to .lp
            subprocess.run(["python", "pkl_to_lp.py", input_pkl, output_lp])

            # Run clingo with helper.lp and scheduler.lp and save the output
            clingo_command = f"clingo ../encodings/helper.lp ../encodings/scheduler.lp {output_lp}"
            subprocess.run(clingo_command, stdout=open(output_txt, 'w'), shell=True)

            print(f"Processed: {input_pkl} | Output saved to: {output_txt}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python automation.py input_directory")
        sys.exit(1)

    input_directory = sys.argv[1]

    # Create the 'test' directory in the directory above
    test_directory = "test"
    if not os.path.exists(test_directory):
        os.makedirs(test_directory)

    process_directory(input_directory)
