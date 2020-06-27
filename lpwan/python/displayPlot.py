#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str,
                        help="name of input file")
    parser.add_argument("-o", "--out", type=str,
                        help="name of output file")
    parser.add_argument("-a", "--abs", action='count',
                        help="generate magnitude output")
    parser.add_argument("-i", "--index", action='count',
                        help="show index instead of time")
    args = parser.parse_args()
    f = np.load(args.inputfile)

    if args.index:
        t = np.arange(f['data'].size)
    else:
        t = f['t0'] + np.arange(f['data'].size)*f['Ts']
    plt.figure()
    if args.abs:
        plt.plot(t, np.abs(f['data']), "C0-", label="abs")
    else:
        plt.plot(t, f['data'].real, "C0-", label="real")
        plt.plot(t, f['data'].imag, "C1-", label="imag")
    plt.xlabel("time (s)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    if args.out:
        plt.savefig(args.out, format='pdf')

    # plt.draw()
    plt.show()