from numpy import fft
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import numpy as np

def plotFFT(data, fig, xscal=1):
    fig.clf()
    p=fig.add_axes([0.1, 0.1, 0.8, 0.8])
#    p.set_title("FFT")
    transf=np.abs(fft.rfft(data))
    
    fscaler=0.5/(xscal*2*np.pi) 

    maxv=max(transf)
    maxf=np.where(transf==maxv)[0][0]*fscaler

    p.set_title("FFT, fmax="+str(maxf)+" Hz")
    p.plot(np.multiply(list(range(len(transf))),fscaler),transf)
    #p.set_xlim([0,40000])
    p.set_xlabel("Hz")
    p.grid()
    
