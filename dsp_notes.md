## TODO
- Put NoisePlot is a seperate module to reuse
- Code to graph signals like in an EQ
  - x axis is freq, y is amplitude
  - need to use fft of some sort?
  - how to live update the graph?
  - feed it the data frames?
  - put it on a different thread?
  - [Matplot Power Spectral Density](https://matplotlib.org/stable/gallery/lines_bars_and_markers/psd_demo.html#sphx-glr-gallery-lines-bars-and-markers-psd-demo-py)
  - what is power spectral density?
  - spectrum of infinite time signal?


## Python
- What is a "Queue", and why do we use it?
  - used to pass infomartion betwen threads
  - First In First Out queue
  - Last In First Out queue
  - Priority queue where entries are kept sorted
  - How we use a Queue
  - create FIFO queue object: q = queue.Queue
  - put stuff in the queue q.put(stuff)
  - take stuff from the queue q.get()
  - take stuff if it is available no wait q.get_nowait()
  - Use Cases: pass data from call back to a graph
- What is "Deque", and why do we use it?
- Passing a queue into a class
`class NoisePlot(QtWidgets.QMainWindow):
      def __init__(self, data_queue, fs, downsample, window_ms):
          super().__init__()
          self.q = data_queue `
  - 'data_queue' is a refernce to the queue outside the class not a copy
  - python objects are 'mutable' so assignment binds another name to the same object
  - read more about 'mutable' objects in python
- Create a circular buffer using Deque??


## DSP Programming
- How to pass audio data from real time audio call back to NRT threads for graphs etc?
  - lock-free ring buffers aka circular buffers to move data between threads
  - python does not have lock-free ring buffers due to GIL
- FIFO: first in first out. in relation to a que or buffer


## FFT
[JUCE FFT Tutorial](https://juce.com/tutorials/tutorial_simple_fft/)
- What is the 'order' of the FFT?
  - the size of the window
  - the number of points the FFT will operate on is 2^order
  - why?
  - it's convered to binary??
- numpy fft
  - what do the values returned by fft represent?
  - is it the amplitude at that freq?
  - how do you get the power at each frequency?
> When the input a is a time-domain signal and A = fft(a), np.abs(A) is its amplitude spectrum and np.abs(A)**2 is its power spectrum.
  - how do you get the frequencies returned by the fft?
  - Could I use rfft becuase the input is strictly real?
> When the input is purely real, its transform is Hermitian, i.e., the component at frequency is the complex conjugate of the component at frequency
, which means that for real inputs there is no information in the negative frequency components that is not already available from the positive frequency components. The family of rfft functions is designed to operate on real inputs, and exploits this symmetry by computing only the positive frequency components, up to and including the Nyquist frequency. Thus, n input points produce n/2+1 complex output points. The inverses of this family assumes the same symmetry of its input, and for an output of n points uses n/2+1 input points.
-fft returns the same number of frequency buckets as n samples passed to it
-for n time series data points, fft returns n frequency data points
- fft is symetric so half of these are the negative frequencies
- when we graph the PSD we have the freq >1
