"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, start_frequency=88000000, sample_rate=10000000, vector_size=1024):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Freq Getter',   # will show up in GRC
            in_sig=[(np.float32, vector_size)],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.vector_size = vector_size
        self.start_frequency = start_frequency
        self.sample_rate = sample_rate
        self.peakfreaks = []
    def work(self, input_items, output_items):
        idxs = np.flatnonzero(input_items[0][0])
        peaks = self.start_frequency + (self.sample_rate/self.vector_size * idxs)
        self.peakfreaks = [str(i) for i in peaks]
      
        return 1
    def getFreqs(self):
        return self.peakfreaks
