import clingo
import os
import argparse
import time
from pathlib import Path
import threading

import pkl_to_lp


class Ins_Runner:

    def __init__(self, ins_files, encodings, out_dir, time_limit, optimize, id):
        self._ins_files = ins_files
        self._encodings = encodings
        self._out_dir = out_dir
        self._time_limit = time_limit
        self._opt = optimize
        self._id = id

        self._model = None
        self._cost = None
        self._last_model_time = None

    def _on_model(self, model):
        self._last_model_time = time.time()
        self._model = model.symbols(shown=True)
        self._cost = model.cost
        print(model.cost)
        # stop search on first solution if not opt option
        return self._opt

    def get_transraw_count(self, lp_ins):
        with open(lp_ins, 'r') as f:
            lines = f.readlines()
            transraw_count = sum(1 for line in lines if line.startswith('transraw'))
        return transraw_count

    def estimate_slimit(self, lp_ins):
        transraw_count = self.get_transraw_count(lp_ins)
        return min(18 + transraw_count//10, 30)  

    def convert_instance(self, pkl_ins):
        tmp_ins = "./tmp.lp"
        pkl_to_lp.main([None, str(pkl_ins), tmp_ins])
        return tmp_ins

    def check_time(self, ctl, done):
        # check every 5 seconds for time_out
        start_t = time.time()
        while time.time() - start_t <= self._time_limit and not done.isSet():
            done.wait(5)
        if not done.isSet():
            print("Time-out")
            ctl.interrupt()

    def main(self):
        for ins in self._ins_files:
            self._model = None
            self._cost = None
            self._last_model_time = None

            print(ins)
            tmp_ins = self.convert_instance(ins)
            slimit = self.estimate_slimit(tmp_ins)
            ctl = clingo.Control([f"-c slimit={slimit}"])
            ctl.load(tmp_ins)
            os.remove(tmp_ins)
            for path in self._encodings:
                ctl.load(str(path))
    
            done = threading.Event()
            t1 = threading.Thread(target=self.check_time, args=(ctl, done))
            t1.start()

            s_time = time.time()
            ctl.ground([("base", [])], context=self)
            g_time = time.time()
            solve_res = ctl.solve(on_model=self._on_model)
            if solve_res.interrupted or solve_res.satisfiable:
                done.set()
                t1.join()
                if self._id is None:
                    out_p = f"{str(self._out_dir)}/{os.path.basename(ins)[:-4]}_res.txt"
                else:
                    out_p = f"{str(self._out_dir)}/{os.path.basename(ins)[:-4]}_{self._id}_res.txt"
                if os.path.exists(out_p):
                    os.remove(out_p)
                out_f = open(out_p, "w")
                if solve_res.interrupted:
                    out_f.write("Time-out after {}s.\n".format(self._time_limit))
                    out_f.write("Following times are only estimations.\n")
                    out_f.write("Grounding time: {}\n".format(g_time - s_time))
                    if self._last_model_time:
                        out_f.write("Last model found after {}s since search start.\n".format(self._last_model_time))
                        out_f.write("{} using {}, search optimum: {}\n".format(ins, list(map(str, self._encodings)), self._opt))
                        out_f.write("Answer:\n{}\nCost: {}\n".format(" ".join([str(atom) for atom in self._model]), self._cost[0]))
                    else:
                        out_f.write("No model found.\n")
                else:
                    out_f.write("{} using {}, search optimum: {}\n".format(ins, list(map(str, self._encodings)), self._opt))
                    out_f.write("Answer:\n{}\nCost: {}\n".format(" ".join([str(atom) for atom in self._model]), self._cost[0]))
                    out_f.write("Choices: {}\n".format(ctl.statistics["solving"]["solvers"]["choices"]))
                    out_f.write("Conflicts: {}\n".format(ctl.statistics["solving"]["solvers"]["conflicts"]))
                    out_f.write("Grounding time: {}\n".format(ctl.statistics["summary"]["times"]["total"] - ctl.statistics["summary"]["times"]["solve"]))
                    out_f.write("Solving time: {}\n".format(ctl.statistics["summary"]["times"]["solve"]))
                out_f.close()
            else:
                print("UNSAT")
                done.set()
                t1.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run .pkl instances in ins_dir with given encodings and save results in out_dir.')
    parser.add_argument('ins_dir', type=Path, metavar='INS', help='instance directory')
    parser.add_argument('out_dir', type=Path, metavar='OUT', help='output directory')
    parser.add_argument('encodings', type=Path, metavar='ENC', nargs='+', help='encoding to be used.')
    parser.add_argument('--optimize', action='store_true', help='find optimal solution.')
    parser.add_argument('--time-limit', type=int, default=1800, metavar="N", help='time limit in seconds.')
    parser.add_argument('--id', type=str, help='additional identifier of result file.')
    
    args = parser.parse_args()

    if not os.path.exists(args.out_dir):
        os.makedirs(args.out_dir)

    ins_files = list(args.ins_dir.glob('*.pkl'))
    runner = Ins_Runner(ins_files, args.encodings, args.out_dir, args.time_limit, args.optimize, args.id)
    runner.main()
    print("All done")