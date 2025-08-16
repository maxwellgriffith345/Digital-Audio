## TODO
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


## DSP Programming
- How to pass audio data from real time audio call back to NRT threads for graphs etc?
  - lock-free ring buffers aka circular buffers to move data between threads
  - python does not have lock-free ring buffers due to GIL
