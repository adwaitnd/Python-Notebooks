# channel simulation tools
import scipy.constants as const
import numpy as np


# helper functions (only usable internally)

def __maxFreqIndex(n):
    return int(n-1)//2


def __minFreqIndex(n):
    return __maxFreqIndex(n) + 1


def __fftIndex(n, f, fs):
    """The FFT bin index of a frequency. Frequencies out of bounds are
    clipped. The i-th bin goes from (i/n)*fs to ((i+1)/n)*fs for positive
    frequencies. TODO: describe bins for negative frequncies

    Args:
        n ([type]): [description]
        f ([type]): [description]
        fs ([type]): [description]

    Returns:
        [type]: [description]
    """
    if f >= fs/2:
        # out of positive bound
        return __maxFreqIndex(n)
    elif f <= -fs/2:
        # out of negative bound
        return __minFreqIndex(n)
    else:
        # valid frequency
        if f >= 0:
            return int(n*(f/fs))
        else:
            return int(n*(f/fs + 1))

# library functions (usable from elsewhere)

# channel modification functions


def addResponse(CH, dist, resp, Ts):
    """[summary]

    Args:
        CH ([type]): [description]
        dist ([type]): [description]
        resp ([type]): [description]
        Ts ([type]): [description]
    """

    def propTime(dist):
        return dist/const.speed_of_light

    tProp = propTime(dist)

    def timeIndex(propTime, Ts):
        return int(np.floor(propTime/Ts))

    ind = timeIndex(tProp, Ts)
    CH[ind] = CH[ind] + resp  # change channel resp in place


def addWhiteNoise(CH, std):
    return CH + np.random.normal(loc=0, scale=std, size=CH.shape)

# common signal processing filters


def idealLowpassFilter_fdomain(n, bw, fs):
    fPosLimit = bw/2
    fNegLimit = - bw/2

    indPosLimit = __fftIndex(n, fPosLimit, fs)
    indNegLimit = __fftIndex(n, fNegLimit, fs)

    lpf = np.zeros(n)
    lpf[0:indPosLimit] = 1.0  # positive frequencies
    lpf[indNegLimit:n] = 1.0  # negative frequencies

    return lpf


def idealLowpass_fdomain(CH_f, bw, fs):
    n = CH_f.shape[-1]
    bpFilter = idealLowpassFilter_fdomain(n, bw, fs)
    return np.multiply(bpFilter, CH_f)


def idealLowpass(CH, bw, fs):
    CH_f = np.fft.fft(CH)
    CH_f = idealLowpass_fdomain(CH_f, bw, fs)
    return np.fft.ifft(CH_f)


def idealBandpassFilter_fdomain(n, fc, bw, fs):
    fPosMin = fc - bw/2
    fPosMax = fc + bw/2
    fNegMin = -fc - bw/2
    fNegMax = -fc + bw/2

    indPosMin = __fftIndex(n, fPosMin, fs)
    indPosMax = __fftIndex(n, fPosMax, fs)
    indNegMin = __fftIndex(n, fNegMin, fs)
    indNegMax = __fftIndex(n, fNegMax, fs)

    bpFilter = np.zeros(n)
    bpFilter[indPosMin:indPosMax] = 1.0
    bpFilter[indNegMin:indNegMax] = 1.0

    return bpFilter


def idealBandpass_fdomain(CH_f, fc, bw, fs):

    n = CH_f.shape[-1]
    bpFilter = idealBandpassFilter_fdomain(n, fc, bw, fs)
    return np.multiply(bpFilter, CH_f)


def idealMultipass_fdomain(CH_f, fcList, bw, fs):
    n = CH_f.shape[-1]
    bpFilter = np.zeros(n)
    for fc in fcList:
        bpFilter = bpFilter + idealBandpassFilter_fdomain(n, fc, bw, fs)
    return np.multiply(bpFilter, CH_f)


def idealBandpass(CH, fc, bw, fs):
    CH_f = np.fft.fft(CH)
    CH_f = idealBandpass_fdomain(CH_f, fc, bw, fs)
    return np.fft.ifft(CH_f)


def idealMultipass(CH, fcList, bw, fs):
    CH_f = np.fft.fft(CH)
    CH_f = idealMultipass_fdomain(CH_f, fcList, bw, fs)
    return np.fft.ifft(CH_f)


def extractSamples(t, h, tLimits):
    """given a time series with timestamps, extract elements which lie in
    tLow <= t_i < tHigh

    Args:
        t (numpy array): array of sample times, in sorted order
        h (numpy array): array of channel response
        tLimits (list of floats): list with [tStart, tEnd]
    """

    ind = np.searchsorted(t, tLimits)
    return t[ind[0]:ind[1]], h[ind[0]:ind[1]]


def mixer(x, fc, fs, theta0=0.0):
    n = x.shape[-1]
    Ts = 1/fs
    theta = 2*np.pi*fc*np.arange(0, n*Ts, Ts) + theta0
    xI = np.multiply(np.real(x), np.cos(theta))
    xQ = np.multiply(np.imag(x), np.sin(theta))
    return xI + 1j*xQ
