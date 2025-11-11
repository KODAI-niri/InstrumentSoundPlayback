#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Returner : 
オブジェクトを建設する役割を持つ機能群を定義する
モジュールファイル
名前に関して、あらかじめ用意されている予約語やライブラリと被る可能性がある
物に関しては、先頭にreturnをつけています。
そうでない場合は、先頭にreturnはありません
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/23"

import numpy as np

###### about char function ######

def blankChar():
    """
    空白文字を建設して応答する
    """

    return ""

def blueChar():
    """
    'blue'を応答する
    """

    return 'blue'

def greenChar():
    """
    'green'を応答する
    """

    return 'green'

def redChar():
    """
    'red'を応答する
    """

    return 'red'

def yellowChar():
    """
    'yellow'を応答する
    """

    return 'yellow'

###### about none pointer function ######

def nonePointer():
    """
    Noneポインタを建設して応答する
    """

    return None

###### about int function ######

def zeroInt():
    """
    値0を建設して応答する
    """

    return 0

def oneInt():
    """
    値1を応答する
    """

    return 1

def twoInt():
    """
    値2を応答する
    """

    return 2

def threeInt():
    """
    値3を応答する
    """

    return 3

def fourInt():
    """
    値4を応答する
    """

    return 4

def fiveInt():
    """
    値5を応答する
    """

    return 5

###### about bool function ######

def returnTrue():
    """
    Trueを建設して応答する
    """

    return True

def returnFalse():
    """
    Falseを建設して応答する
    """

    return False

###### about list function ######

def emptyList():
    """
    空リストを作成して応答する
    """

    return []

###### about frequencies function ######

def blueFrequencies():
    """
    [220.00, 233.08, 246.94, 256, 261.62, 277.178, 293.66]
    を応答する
    """

    return [220.00, 233.08, 246.94, 256, 261.62, 277.178, 293.66]

def greenFrequencies():
    """
    [349.23, 370.00, 392.00, 408, 415.31, 440.01, 466.17]
    を応答する
    """

    return [349.23, 370.00, 392.00, 408, 415.31, 440.01, 466.17]

def redFrequencies():
    """
    [880.01, 932.33, 987.77, 1027, 1046.51, 1108.74, 1174.67]
    を応答する
    """

    return [880.01, 932.33, 987.77, 1027, 1046.51, 1108.74, 1174.67]

def yellowFrequencies():
    """
    [554.36, 587.33, 622.25, 647, 659.25, 698.45, 739.98]
    を応答する
    """

    return [554.36, 587.33, 622.25, 647, 659.25, 698.45, 739.98]

###### about data function ######

def soundWaveData():
    """
    音波を作成するのに必要なデータを応答する
    """

    return {
        "sampling_rate": 44100,
        "duration": 1.0,
        "num_samples": 44100,
        "dt": 1.0/44100,
        "sound_speed": 343
    }

def returnTimeData():
    """
    timeデータを応答します
    """

    sound_wave_data = soundWaveData()

    return np.linspace(0, sound_wave_data["duration"], 
                       int(sound_wave_data["sampling_rate"] * sound_wave_data["duration"]),
                       endpoint=returnFalse())

###### about ADSREnvelop function ######

def ADSREnvelopFloatValue(attack : float, decay : float,
                          sustain : float, release : float):
    """
    ADSRの値を応答する
    Arguments:
        attack : 最大音までの時間
        decay : 最大音からの減少時間
        sustain : 音持続量
        release : 音がなくなるまでの時間
    """

    return {
        "attack": attack,
        "decay": decay,
        "sustain": sustain,
        "release": release
    }

def ADSREnvelopTimeData(adsr_envelop : dict, 
                        time_data, sound_data : dict):
    """
    ADSRの時間軸データを応答する
    Arguments:
        adsr_envelop : ADSREnvelop
        time_data : 時間軸データ
        sound_data : サウンドデータ
    """

    env = np.zeros_like(time_data)

    a_samples = int(sound_data["sampling_rate"] * adsr_envelop["attack"])
    d_samples = int(sound_data["sampling_rate"] * adsr_envelop["decay"])
    r_samples = int(sound_data["sampling_rate"] * adsr_envelop["release"])
    s_samples = int(len(time_data) - (a_samples + d_samples + r_samples))

    env[:a_samples] = np.linspace(zeroInt(),
                                   oneInt(), a_samples, 
                                   endpoint=returnFalse())
    env[a_samples:a_samples+d_samples] = np.linspace(oneInt(), 
                                                     adsr_envelop["sustain"],
                                                     d_samples, 
                                                     endpoint=returnFalse())
    env[a_samples+d_samples:a_samples+d_samples+s_samples] = adsr_envelop["sustain"]
    env[-r_samples:] = np.linspace(adsr_envelop["sustain"], 
                                   zeroInt(),
                                   r_samples,
                                   endpoint=returnFalse())
    return env

###### about electronic guitar function ######

def electronicGuitarData():
    """
    エレクトリックギターのデータを応答します
    """

    return {
        "pluck_position": 0.2,
        "pluck_force": 1.0,
        "pickup_position": 0.3,
        "inductance": 3e-3,
        "resistance": 5e3,
        "capatitance": 200e-12
    }

def electronicGuitarADSRFloatValue():
    """
    エレクトリックギターのADSRを応答します
    """

    return ADSREnvelopFloatValue(0.01, 0.0, 0.2, 0.01)

def electronicGuitarADSRTimeData():
    """
    エレクトリックギターのADSR時間軸データを応答します
    """

    adsr_envelop = electronicGuitarADSRFloatValue()
    time_data = returnTimeData()
    sound_data = soundWaveData()

    return ADSREnvelopTimeData(adsr_envelop, time_data, sound_data)

###### about reggae organ function ######
    
def returnReggaeAmplitude():
    """
    レゲエオルガンの振幅の群れを応答します
    """

    return [1.0, 0.6, 0.3, 0.2, 0.1]

def returnReggaeHarmonics():
    """
    レゲエオルガンの倍音の群れを応答します
    """

    harmonics = []

    harmonics.append(oneInt())
    harmonics.append(twoInt())
    harmonics.append(threeInt())
    harmonics.append(fourInt())
    harmonics.append(fiveInt())

    return harmonics

def reggaeADSREnvelopFloatValue():
    """
    レゲエオルガンに用いるADSREnvelopの値を応答する
    """

    return ADSREnvelopFloatValue(0.02, 0.10, 0.1, 0.10)

def reggaeADSREnvelopTimeData():
    """
    レゲエオルガンに用いるADSREnvelopの時間軸データを応答する
    """

    adsr_envelop = reggaeADSREnvelopFloatValue()
    time_data = returnTimeData()
    sound_data = soundWaveData()
    
    return ADSREnvelopTimeData(adsr_envelop, time_data, sound_data)

###### about oboe function ######

def oboeData():
    """
    オーボエに関するデータを辞書形式で応答します
    """

    return {
        "blowing_pressure": 0.6,
        "reed_stiffness": 72,
        "tube_length": 0.7,
        "alpha": 0.3,
        "threshold": 0.3,
        "rho": 1.204,
        "reflection": -0.001
    }

###### about trumpet function ######

def trumpetData():
    """
    トランペットに関するデータを辞書形式で応答します
    """

    return {
        "blowing_pressure": 0.6,
        "lip_mass": 0.002,
        "damping": 1.0,
        "blowing_pressure": 2000,
        "mouse_open_area_scale": 1e-4,
        "rho": 1.204,
        "tube_length": 1.48,
        "a0": 1e-6,
        "a1": 1e-4,
        "a2": 0.0,
        "Z_scale": 1e-1,
        "r_mouth": -0.95,
        "r_bell": 0.0,
        "mp_effective_length": 0.0,
        'use_impedance_conversion': True,
        'injected_scale': 1e-5
    }

###### about ukulele function ######

def ukuleleData():
    """
    ウクレレに関するデータを辞書形式で応答する
    """

    return {
        "string_tension": 60.0,
        "string_density": 0.01,
        "pluck_position": 0.2,
        "pluck_force": 1.0,
        "damping": 0.996,
        "body_resonance": [100, 300, 800]
    }

def ukuleleADSREnvelopFloatValue():
    """
    ウクレレのエンベロープの値を応答する
    """

    return ADSREnvelopFloatValue(0.01, 0.5, 0.3, 0.5)

def ukuleleADSREnvelopTimeData():
    """
    ウクレレのエンベロープの時間軸データを応答する
    """

    adsr_envelop = ukuleleADSREnvelopFloatValue()
    time_data = returnTimeData()
    sound_data = soundWaveData()
    
    return ADSREnvelopTimeData(adsr_envelop, time_data, sound_data)

###### about flute function ######

def fluteData():
    """
    フルートに関するデータを辞書形式で応答する
    """

    return {
        "blowing_pressure": 0.4,
        "jet_delay": 0.25,
        "damping": 0.999,
        "noise_level": 0.02
    }

###### about japaneseGuitar function ######

def japaneseGuitarData():
    """
    三味線に関するデータを辞書形式で応答する
    """

    return {
        "pick_force": 1.0,
        "damping": 0.995,
        "pick_position": 0.2, 
        "body_modes": [250, 500, 1200, 2000]
    }

###### about violin function ######

def violinData():
    """
    ヴァイオリンに関するデータを辞書形式で応答する
    """

    return {
        "bow_pressure" : 0.4,
        "bow_velocity" : 0.3,
        "string_tension" : 0.8,
        "damping" : 0.998,
        "reflection_coeff" : 0.9
    }

###### about vibraphone function ######

def vibraphoneData():
    """
    ビブラフォンに関するデータを辞書形式で応答する
    """

    return {
        "mallet_force": 1.0,
        "mallet_size": 0.3,
        "strike_position": 0.2,
        "damping": 0.998,
        "vibrato_rate": 6.0,
        "vibrato_depth": 0.02,
        "f_n": [1.0, 2.756, 5.404, 8.933, 13.333]
    }

###### about piano function ######

def pianoData():
    """
    ピアノに関するデータを辞書形式で応答する
    """

    return {
        "hammer_force": 50.0,
        "hammer_mass": 0.008,
        "string_tension": 800.0,
        "damping": 0.996,
        "pedal": 0.0, # データとして束縛するが、個別で名前空間に束縛させる
        "string_position": 0.15, 
        "hammer_position": -0.002,
        "resonant_filters": [50, 100, 200, 350, 450, 700, 1000, 1200], 
        "string_lengthes": [1.8, 1.4, 1.1, 0.9, 0.8, 0.7, 0.6],
        "force_time": 0.02,
    }

def pianoResonator():
    """
    ピアノの共鳴フィルタを作成し、応答します
    """

    class PianoResonator:
        """
        ピアノの共鳴フィルタクラス
        """

        def __init__(self, Q = 10, gain=1.0):
            """
            このクラスのコンストラクタ
            """

            self.Q = Q
            self.gain = gain

            self.y1 = 0.0
            self.y2 = 0.0
        
        def setFrequency(self, f0):
            """
            周波数を設定します
            """

            self.f0 = f0
        
        def setSamplingRate(self, fs):
            """
            サンプリング周波数を設定します
            """

            self.fs = fs
        
        def defineOtherProperties(self):
            """
            プロパティの群れを定義します
            """

            self.omega = 2.0 * np.pi * self.f0 / self.fs
            self.r = np.exp(-np.pi * self.f0 / (self.Q * self.fs))
            self.a1 = 2.0 * self.r * np.cos(self.omega)
            self.a2 = - (self.r**2)
            self.b0 = (1.0 - self.r) * self.gain
        
        def process(self, x):
            """
            共鳴フィルタを掛けます
            Arguments:
                x : 値
            """

            y = self.a1 * self.y1 + self.a2 * self.y2 + self.b0 * x
            self.y2 = self.y1
            self.y1 = y
            return y
    
    return PianoResonator()