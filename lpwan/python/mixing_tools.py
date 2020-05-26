import numpy as np
import scipy.signal as sig

# From a wideband waveform, shift a band of selected frequencies towards the center
#
# This is to be done in two ways:
# 1. shift a single sided band towards the baseband. the center frequency represents the beginning of the frequency band
# 2. shift a double sided band. the center frequency represents the middle of the frequency band
#

# data import functions for USRP binary files
# (loading functions are tested - May 24)
def load_IQBinary_float32(file):
    # I and Q are both 32 bit floats
    return np.fromfile(file, dtype=np.complex64)


def load_IQBinary_float64(file):
    # I and Q are both 32 bit floats
    return np.fromfile(file, dtype=np.complex128)


def load_IQBinary_int8(file):
    # I and Q are both 8 bit ints
    x = np.fromfile(file, dtype=np.int8)
    x = x[0::2] + 1j*x[1::2]
    return x.astype('complex64')


def load_IQBinary_int16(file):
    # I and Q are both 16 bit ints
    x = np.fromfile(file, dtype=np.int16)
    x = x[0::2] + 1j*x[1::2]
    return x.astype('complex64')


# FFT frequency bucket indexing functions
# (tested for odd/even sized time series and on positive and negative frequencies- May 25)

# Note: rounding is performed to eliminate problems from floating point math adding any errors before conversion to integers. Rounding precision of 0.001 was selected arbitrarily but seemed reasonable.

# f is frequency to find index for
# n is number of samples in fft
# Ts is sampling time
# fc is center frequency (if the requested frequency is not baseband)

# given a positive freq, find the indice of the closest FFT bucket <= requested freq
def fpos2indFloor(f, n, Ts, fc=0):
    return int(np.floor(np.round(n*(f-fc)*Ts, 3)))


# given a positive freq, find the indice of the closest FFT bucket >= requested freq
def fpos2indCeil(f, n, Ts, fc=0):
    return int(np.ceil(np.round(n*(f-fc)*Ts, 3)))


# given a negative freq, find the indice of the closest FFT bucket <= requested freq
def fneg2indFloor(f, n, Ts, fc=0):
    return int(n + np.floor(np.round(n*(f+fc)*Ts, 3)))


def fneg2indCeil(f, n, Ts, fc=0):
    return int(n + np.ceil(np.round(n*(f+fc)*Ts, 3)))

# TODO: signal mixing functions

# these operate on frequency data. Another function is responsible for converting time series data into frequency data
def fft_basebandShift_singleSided(fftdata, indStart, nBuckets):
    # NOTE: this does not work. We may not even need this
    n = fftdata.size
    # fbb = np.zeros(2*nBuckets)
    # fbb[0:nBuckets] = fftdata[indStart:(indStart+nBuckets)]
    # fbb[nBuckets:] = fftdata[(n-(indStart+nBuckets)):(n-indStart)]
    fbb = np.concatenate((fftdata[indStart:(indStart+nBuckets)],
                          fftdata[(n-(indStart+nBuckets)):(n-indStart)]))
    return fbb


# generic matched filter function
def matchedFilter(data, template, mode='full'):
    m = np.flipud(np.conj(template))
    np.convolve(data, m, mode=mode)


#
def chirpMF(data, fc, fs, fcChirp, bw, TChirp):
    pass
