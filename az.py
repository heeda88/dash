#%%
__author__ = 'heeda'

from random import sample
import pandas as pd
import numpy as np
from scipy.io import wavfile
import binascii
import struct
from glob import glob
import librosa.display
import matplotlib.pyplot as plt
import librosa
from tqdm import tqdm


class namuAudio(object):
    """
    == : Title
    -- : subtitle

    오디오파일 분석
    ===========

    .. _refrence_link:
      https://youngq.tistory.com/77
      http://soundfile.sapp.org/doc/WaveFormat/

    Attributes:
      filepath = filepath
      x= pcm data
      sr= sample rate
      X= pcm data to Fourier Transform
      l1= wave form meta data first line 
      l2 = wave form meta data second list

    Example:
      예시를 기록합니다.

    Todo:
      * 파일 호출, 메타 데이터 분석, 시각화
      * 데이터 비교
  """

    def __init__(self, filepath):
        self.filepath = filepath
        self.x, self.sr = librosa.load(path=self.filepath, sr=44100)
        # Fourier
        self.X = librosa.stft(y=self.x)
        self.Xdb = librosa.amplitude_to_db(S=abs(self.X))
        f = open(self.filepath, 'rb')
        self.l1 = f.readline()
        self.l2 = f.readline()
        f.close()
    def getAudio(self):
        return self.x, self.sr

    def getWaveplot(self):
        plt.figure(figsize=(14, 5))
        librosa.display.waveplot(y=self.x, sr=self.sr)

    def getSpectogram(self):
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(data=self.Xdb,
                                 sr=self.sr,
                                 x_axis='time',
                                 y_axis='hz')
        plt.colorbar()

    def getSpectogramLog(self):
        plt.figure(figsize=(14, 5))
        librosa.display.specshow(data=self.Xdb,
                                 sr=self.sr,
                                 x_axis='time',
                                 y_axis='log')
    def wavFormat(self):
        print(self.l1)
        print(self.l2)

    def fileSize(self):
        size = self.l1[4:8]
        if len(size) == 4:
            data = struct.pack('<I', int(binascii.b2a_hex(size), 16))
            hexa_size = binascii.b2a_hex(data)
            byte_size = (int(hexa_size, 16) + 8)
            Megabyte_size = byte_size / 1000000
            return Megabyte_size
        else:
              data = struct.pack('<h', int(binascii.b2a_hex(size), 16))
              hexa_size = binascii.b2a_hex(data)
              byte_size = (int(hexa_size, 16) + 8)
              Megabyte_size = byte_size / 1000000
              return Megabyte_size

    def getID(self):
        ID = self.l1[0:4]
        if len(ID) == 4:
            data = struct.pack('<I', int(binascii.b2a_hex(ID), 16))
            return binascii.b2a_hex(data)
        else:
            data = struct.pack('<h', int(binascii.b2a_hex(ID), 16))
            return binascii.b2a_hex(data)

    def getFormat(self):
        Format = self.l1[8:12]
        if len(Format) == 4:
            data = struct.pack('<I', int(binascii.b2a_hex(Format), 16))
            return binascii.b2a_hex(data)
        else:
            data = struct.pack('<h', int(binascii.b2a_hex(Format), 16))
            return binascii.b2a_hex(data)

    def getDuratrion(self):
        duration=round(len(self.x)/self.sr,4)
        return duration

    def getMetaInfo(self):
      size=self.fileSize()
      duration=self.getDuratrion()
      return [self.sr,duration,size]



if __name__ == '__main__':

    wav_list = glob('/data/namu/deafness/sample/데이터/전남대학교/2022.02.09/wav/*.wav')
    good_file = '/data/namu/deafness/SineWaveMinus16.wav'
    columns=['region','timestamp','uid','sex','age','period','r_ear_loss','l_ear_loss','datasets','text','LabelBoolean']
    metainfo=['samplerate','duration','size(MB)']
    df=pd.DataFrame()
    df.loc[:,'filepath']=wav_list
    df.loc[:,'filename']=df.loc[:,'filepath'].astype('str').str.split(pat='/').str[-1]
    df.loc[:,metainfo]=[ namuAudio(index).getMetaInfo() for index in tqdm(wav_list)]
    df.loc[:,columns[:]]=df.loc[:,'filename'].astype('str').str.split(pat='-').str[:].tolist()
    columns=columns+['filepath','filename','size(MB)','samplerate','duration']
    df=df.loc[:,columns]
    df.loc[:,'LabelBoolean']=df.loc[:,'LabelBoolean'].str.split(pat='.wav').str[0]
    df.to_csv('row_data.csv',index=False, encoding='utf-8')
