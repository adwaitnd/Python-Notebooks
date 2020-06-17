#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("script started")
    x = np.arange(2, 3, 0.1)
    plt.figure()
    plt.plot(x, 'b.-', label="x")
    plt.legend()
    plt.draw()
    print("script done")
    plt.show()
