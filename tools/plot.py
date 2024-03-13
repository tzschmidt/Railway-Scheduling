import matplotlib.pyplot as plt
import argparse
from pathlib import Path
import os



def main(out, dirs, mode, upper_limit, log):
    modes = {
        "solve-time in s": 3,
        "ground-time in s": 2,
        "choices": 0,
        "conflicts": 1
    }
    max = 0
    instances = []
    for f in list(dirs[0].glob('*.txt')):
        instances.append(str(os.path.basename(f)).split("_", 1)[0])
    results = dict.fromkeys(list(map(os.path.basename, dirs)))
    for dir in dirs:
        enc = os.path.basename(dir)
        ins_res = {}
        for ins in list(dir.glob('*.txt')):
            ins_name = str(os.path.basename(ins)).split("_", 1)[0]
            if ins_name in instances:
                with open(ins, 'r') as f:
                    res = float((f.readlines()[4:][modes[mode]]).split(":")[1])
                f.close()
                ins_res[ins_name] =  res
                if res > max:
                    max = res
        enc_res = []
        for i in instances:
            if i in ins_res:
                enc_res.append(ins_res[i])
            else:
                # some extremely high value
                enc_res.append(max*1000000)
        results[enc] = enc_res
    
    x = [i for i in range(len(instances))]  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots()

    for encoding, result in results.items():
        offset = width * multiplier
        rects = ax.bar(list(map(offset .__add__, x)), result, width, label=encoding)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel(mode)
    if log:
        ax.set_yscale("log")
    ax.set_title('Results grouped by instance')
    plt.xticks(list(map(width .__add__, x)), labels=instances, rotation=45, ha="right")
    ax.legend(loc='upper left')
    if upper_limit:
        max = upper_limit
    ax.set_ylim(0, max)

    plt.tight_layout()
    plt.savefig(out, format="pdf", transparent=True)
    plt.show()
        
def check_pdf(file):
    ext = os.path.splitext(file)[1][1:]
    if ext != "pdf":
       parser.error("Specified file is not a .pdf file")
    return file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot results of given directories.')
    parser.add_argument('out', type=lambda s:check_pdf(s), metavar='OUT', help='output .pdf name.')
    parser.add_argument('dirs', type=Path, metavar='IN', nargs="+", help='input directories.')
    parser.add_argument('--solve-time', action='store_true', help='compare solve time.')
    parser.add_argument('--ground-time', action='store_true', help='compare ground time.')
    parser.add_argument('--choices', action='store_true', help='compare number of choices.')
    parser.add_argument('--conflicts', action='store_true', help='compare number of conflicts.')
    parser.add_argument('--upper-limit', type=int, metavar='N', help='set upper limit of the plot.')
    parser.add_argument('--log', action='store_true', help='use logarithmic scale.')
    args = parser.parse_args()

    if args.solve_time:
        main(args.out, args.dirs, "solve-time in s", args.upper_limit, args.log)
    if args.ground_time:
        main(args.out, args.dirs, "ground-time in s", args.upper_limit, args.log)
    if args.choices:
        main(args.out, args.dirs, "choices", args.upper_limit, args.log)
    if args.conflicts:
        main(args.out, args.dirs, "conflicts", args.upper_limit, args.log)




