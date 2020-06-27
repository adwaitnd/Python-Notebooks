#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import argparse
import mixing_tools as mtools

def plotDataShort(filename):
    data = mtools.load_IQBinary_int16(filename)
    print("processing data from ", filename)
    fs = 1.0e6  # sampling frequency of reception
    fcRX = 904.75e6  # center frequency of RX mixer
    fcTX = 905.0e6  # center frequency of TX
    bwChirp = 125.0e3  # bandwidth of LORA transmission
    sf = 9  # spreading factor of chirp signal
    Ts = 1/fs
    
    n = data.size
    t = np.arange(n)*Ts
    
    plt.figure()
    plt.plot(t, data.real, "C0-", label="real")
    plt.plot(t, data.imag, "C1-", label="imag")
    plt.grid()
    plt.legend()
    plt.xlabel("time (s)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("inputfile", type=str,
                        help="name of input file")
    parser.add_argument("-o", "--out", type=str,
                        help="name of output file")
    parser.add_argument("--fs", type=float, default=1e6,
                        help="sampling time")
    parser.add_argument("-a", "--abs", action='count',
                        help="generate magnitude output")
    parser.add_argument("-i", "--index", action='count',
                        help="show index instead of time")
    args = parser.parse_args()

    data = mtools.load_IQBinary_int16(args.inputfile)
    Ts = 1/args.fs
    n = data.size
    t = np.arange(n)*Ts
    if args.index:
        t = np.arange(n)
    else:
        t = np.arange(n)*Ts
    plt.figure()
    if args.abs:
        plt.plot(t, np.abs(data), "C0-", label="abs")
    else:
        plt.plot(t, data.real, "C0-", label="real")
        plt.plot(t, data.imag, "C1-", label="imag")
    plt.xlabel("time (s)")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    if args.out:
        plt.savefig(args.out, format='pdf')

    # plt.draw()
    plt.show()