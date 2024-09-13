from numpy import fft
from matplotlib import pyplot as plt
from matplotlib.figure import Figure


def plotFFT(data, fig):
    fig.clf()
    p=fig.add_axes([0.1, 0.1, 0.8, 0.8])
    p.set_title("FFT")
    p.plot(fft.rfft(data))
    p.grid()
    
