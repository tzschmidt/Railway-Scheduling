import subprocess
import sys
import os
import re

def generate_output_filename(input_file, extension):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    return f"test/{base_name}_output.{extension}"

def get_transraw_count(input_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
        transraw_count = sum(1 for line in lines if line.startswith('transraw'))
    return transraw_count

def calculate_limit(output_lp):
    transraw_count = get_transraw_count(output_lp)
    return min(18 + transraw_count//10, 30)  

def parse_output_txt(output_txt):
    with open(output_txt, 'r') as f:
        lines = f.readlines()
        for line in reversed(lines):  # Start from the bottom
            match = re.search(r"Time\s*:\s*([\d.]+)s", line)
            if match:
                return float(match.group(1))
    return None

def process_directory(directory):
    results = []  # To store results for all instances
    for filename in os.listdir(directory):
        if filename.endswith(".pkl"):
            input_pkl = os.path.join(directory, filename)
            
            # Generate the output file names based on the input file name
            output_lp = generate_output_filename(input_pkl, "lp")
            output_txt_scheduler = generate_output_filename(input_pkl, "scheduler.txt")
            output_txt_scheduler_first = generate_output_filename(input_pkl, "scheduler_first.txt")

            # Convert to .lp
            subprocess.run(["python", "pkl_to_lp.py", input_pkl, output_lp])

            # Calculate the slimit for 
            limit = calculate_limit(output_lp)

            # Run clingo with helper.lp and scheduler.lp and save the output
            clingo_command_scheduler = f"clingo ../encodings/helper.lp ../encodings/scheduler.lp {output_lp} -c slimit={limit}"
            subprocess.run(clingo_command_scheduler, stdout=open(output_txt_scheduler, 'w'), shell=True)

            # Parse output.txt to get the time until optimal answer is found for scheduler.lp
            time_taken_scheduler = parse_output_txt(output_txt_scheduler)

            # Run clingo with helper.lp and scheduler_first.lp and save the output
            clingo_command_scheduler_first = f"clingo ../encodings/helper.lp ../encodings/scheduler_first.lp {output_lp} -c slimit={limit}"
            subprocess.run(clingo_command_scheduler_first, stdout=open(output_txt_scheduler_first, 'w'), shell=True)

            # Parse output.txt to get the time until first answer is found for scheduler_first.lp
            time_taken_scheduler_first = parse_output_txt(output_txt_scheduler_first)

            # Store the results for this instance
            results.append((filename, time_taken_scheduler, time_taken_scheduler_first))

            print(f"Processed: {input_pkl} | Output saved to: {output_txt_scheduler} and {output_txt_scheduler_first} | limit: {limit}")

    # Write results to a results.txt file
    with open("results.txt", "w") as result_file:
        result_file.write("Instance Name\tTime to Optimal (scheduler.lp)\tTime to First (scheduler_first.lp)\n")
        for instance, time_scheduler, time_scheduler_first in results:
            result_file.write(f"{instance}\t{time_scheduler}\t{time_scheduler_first}\n")

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
