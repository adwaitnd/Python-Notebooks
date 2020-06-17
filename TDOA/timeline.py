import numpy as np
import matplotlib.pyplot as plt

class Timeline(Timeseries):
    def __new__(cls, start, stop, step, s0=0.0):
        # generate a timeline of uniformly spaced points between start and stop.
        # the first sample occurs after wall clock time s0
        times = np.arange(start+s0, stop+s0, step)
        obj = super().__new__(cls, input_array=times, tBegin=times[0], ts=step)
        return obj

class CenteredTimeline(Timeseries):
    def __new__(cls, n, step):
        if n%2 == 0:
            start = -(n//2)
            stop = (n//2)
        else:
            start = -((n-1)//2)
            stop = (n//2)
        times = np.arange(start, stop)*step
        obj = super().__new__(cls, input_array=times, tBegin=times[0], ts=step)
        return obj


def cosAligned(timeline, f, t0 = 0.0, phi0 = 0.0):
    # the phase will be phi0 at time t0.
    x = np.cos(2*np.pi*f*(timeline - t0) + phi0)
    return Timeseries(x, timeline.tBegin, timeline.ts)


def sinAligned(timeline, f, t0 = 0.0, phi0 = 0.0):
    # the phase will be phi0 at time t0. t is a time series
    x =  np.sin(2*np.pi*f*(timeline - t0) + phi0)
    return Timeseries(x, timeline.tBegin, timeline.ts)


t = Timeline(start=0, stop=2.0, step=0.001)
x1 = cosAligned(t, f=9.0, t0=0.4)
x2 = cosAligned(t, f=11.0, t0=0.4)

xComb = x1 + x2

tSub = Timeline(start=0, stop=2.0, step=0.02, x0=0.005)

plt.figure()
plt.plot(xComb.sampleTimes(), xComb.data, 'b-')
plt.grid()
plt.tight_layout()
plt.show()