#Play a Note Dispatcher: 

import pyaudio
import wave

Chunk = 1024
Format = pyaudio.paInt16 	#16 Bytes/sample
Channels = 1 				#1 (USING THE MICOPHONE) 
Rate = 44100 				#Typical rate 
writeDuration = 5

#Two octaves of Note paths:
C = "/C.wav"
Cs = "/Cs.wav"
D = "/D.wav"
Eb = "/Eb.wav"
E = "/E.wav"
F = "/F.wav"
Fs = "/Fs.wav"
G = "/G.wav"
Gs = "/Gs.wav"
A = "/A.wav"
Bb = "/Bb.wav"
B = "/B.wav"
C2 = "/C2.wav"
Cs2 = "/Cs2.wav"
D2 = "/D2.wav"
Eb2 = "/Eb2.wav"
E2 = "/E2.wav"
F2 = "/F2.wav"
Fs2 = "/Fs2.wav"
G2 = "/G2.wav"

#Duration has not been implemented
#But ill probably use a for loop to repeat the sound for the desired duration

#Playing the note 
def playC(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + C, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), #We already know the format, but in general, use the builtin 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk)
	#Plays entire audio file
	while len(data) != 0: #Data is a string
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate() 

def playCs(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Cs, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate() 
	
def playD(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + D, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk)  
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()  

def playEb(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Eb, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()  

def playE(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + E, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate() 

def playF(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + F, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()  

def playFs(duration):
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Fs, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate() 

def playG(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + G, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate() 

def playG(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + G, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playGs(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Gs, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playA(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + A, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playBb(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Bb, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playB(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + B, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playC2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + C2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playCs2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Cs2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playD2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + D2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playEb2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Eb2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playE2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + E2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playF2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + F2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playFs2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + Fs2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()

def playG2(duration): 
	p = pyaudio.PyAudio()
	waveFile = wave.open(duration + G2, "rb")
	outStream = p.open(
		format = p.get_format_from_width(waveFile.getsampwidth()), 
		channels = waveFile.getnchannels(),
		rate = waveFile.getframerate(), 
		output = True)
	data = waveFile.readframes(Chunk) 
	while len(data) != 0: 
		outStream.write(data)
		data = waveFile.readframes(Chunk)
	outStream.close() 
	p.terminate()