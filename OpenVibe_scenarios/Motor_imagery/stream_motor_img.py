import numpy
from pylsl import StreamInfo, StreamOutlet

info = StreamInfo('Player_1', 'EEG', 2, 100, 'float32', 'myuid34234')
# next make an outlet
outlet = StreamOutlet(info)
print("now sending data...")

class MyOVBox(OVBox):
	def __init__(self):
		OVBox.__init__(self)
		self.signalHeader = None

        def process(self):
            for chunkIndex in range( len(self.input[0]) ):      
                if(type(self.input[0][chunkIndex]) == OVStreamedMatrixBuffer):
                    chunk = self.input[0].pop()
                    numpyBuffer = numpy.array(chunk)
                    #numpyBuffer = numpyBuffer.mean(axis=0)
                    #chunk = OVSignalBuffer(chunk.startTime, chunk.endTime, numpyBuffer.tolist())
                    print numpyBuffer
                    outlet.push_sample(numpyBuffer)
                    
                elif(type(self.input[0][chunkIndex]) == OVSignalEnd):
                    self.output[0].append(self.input[0].pop())	 
				 			

box = MyOVBox()

