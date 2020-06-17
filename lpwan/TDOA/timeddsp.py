import numpy as np
import scipy.signal as sig


def timesOffset(start, stop, step, offset=0.0, returnStart=False):
    """create a series of times starting with some offset

    Args:
        start (float): start of time series, not considering offset
        stop (float): end of time series. Endpoint not included
        step (float): step size
        offset (float, optional): sampling offset to add to the start and end
            of the series. Defaults to 0.0.
        returnStart (bool, optional): return the sampling time of the first
            sample. Defaults to False.

    Returns:
        numpy.ndarray, float (optional): Returns series of times. Starting time
            of first element
    """

    if returnStart:
        return np.arange(start+offset, stop+offset, step), start+offset
    else:
        return np.arange(start+offset, stop+offset, step)


def cosAligned(times, f, t0 = 0.0, phi0 = 0.0):
    """ Generate a cosine wave

    Args:
        times (numpy 1d array): [description]
        f (float): frequency of the cosine wave
        t0 (float, optional): Starting point of. Defaults to 0.0.
        phi0 (float, optional): [description]. Defaults to 0.0.

    Returns:
        [type]: [description]
    """
    # generate a cosine wave. the phase will be phi0 at time t0.
    x = np.cos(2*np.pi*f*(times - t0) + phi0)
    return x


def sinAligned(times, f, t0 = 0.0, phi0 = 0.0):
    """[summary]

    Args:
        times ([type]): [description]
        f ([type]): [description]
        t0 (float, optional): [description]. Defaults to 0.0.
        phi0 (float, optional): [description]. Defaults to 0.0.

    Returns:
        [type]: [description]
    """
    # generate a sine wave. the phase will be phi0 at time t0.
    x = np.sin(2*np.pi*f*(times - t0) + phi0)
    return x


def chirpPhi(t, cw, t0=0.0, phi0=0.0, w0=0.0):
    # cw is chirp rate = dw/dt = 2*pi*df/dt
    dt = t - t0
    dt2 = np.multiply(t + t0, dt)
    phi = phi0 + (cw/2)*dt2 + (w0 - cw*t0)*dt
    return phi


def bw2slope(bw, tChirp):
    return 2*np.pi*bw/tChirp


def chirpAligned(start, stop, step, bw, cw,
                 t0=0.0, phi0=0.0, w0=0.0, offset=0.0):
    # create a single chirp of bandwidth bw (Hz), with a chirp slope of cw (dw/dt)
    # returns signal and corresponding sampling time

    t = timesOffset(start, stop, step, offset)
    tChirp = 2*np.pi*bw/np.abs(cw)  # time length of chirp
    nChirp = int(np.ceil(tChirp/step)) # max number of samples taken up by chirp
    n0 = int(np.ceil((t0 - start)/step))  # first sample where chirp shows up

    nEnd = n0 + nChirp  # last sample where chirp shows up
    phi = chirpPhi(t[n0:nEnd], cw, t0=t0, phi0=phi0, w0=w0)    
    x = np.zeros(t.shape)
    x[n0:nEnd] = np.cos(phi)

    return t, x
