#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
ElectronicGuitar : 電子的なギター
電子的なギターの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (redChar, redFrequencies,
                               soundWaveData,
                               zeroInt, oneInt, twoInt,
                               electronicGuitarADSRTimeData,
                               electronicGuitarData)

from collections import deque
import numpy as np

from scipy.signal import butter, lfilter

class ElectronicGuitar(Instrument):
    """
    電子的なギタークラス
    Goal:
        赤色の周波数 = 
        [880.01, 932.33, 987.77, 1027, 1046.51, 1108.74, 1174.67]
        の音をリアルに再現する
    Target:
        0: Instrumentクラスを正しく実装する
        1: __init__を実装する
        2: makeSoundを正しく実装する
        3: テストを行う
    """

    def __init__(self):
        """
        このクラスのコンストラクタ
        スーパークラスのコンストラクタを呼び出し、
        自分の色を定義する
        """

        super().__init__()
        self.color = redChar()

    def makeSound(self):
        """
        奏でる音を作成します。
        Target:
            1. サンプリング周波数と周期,周波数群を得る
            2. 周波数ごとに:
                delay_lengthを求め、
                ディレイラインをランダム値で初期化し、
                出力信号配列を準備します。
                その後、
                各サンプル毎に:
                    a. ディレイラインの最初の2つの値を平均する
                    b. 減衰係数を掛ける
                    c. 新しい値を末尾に追加し、古い値を取り除く
            3. 完成した出力信号を返す
        """

        sound_wave_data = soundWaveData()
        red_frequencies = redFrequencies()
        electronicguitar_data = electronicGuitarData()
        adsr_envelop = electronicGuitarADSRTimeData()

        #max_freq = red_frequencies[-1]

        #decay_rate = 0.996

        for frequency in red_frequencies:
            delay_float = sound_wave_data["sampling_rate"] / frequency
            delay_int = int(delay_float)
            #delay_length = int(sound_wave_data["sampling_rate"] / frequency)
            # deque使うのやめる
            #delay_line = deque(np.random.rand(delay_int) * twoInt() - oneInt()) * electronicguitar_data["pluck_force"]
            delay_line = np.random.uniform(-1, 1, delay_int) * electronicguitar_data["pluck_force"]
            delay_line[zeroInt()] += 1.0 # 強めのピックアタック

            #frac = delay_float - delay_int

            #freq_norm = frequency / max_freq
            #decay = decay_rate - 0.005 * freq_norm
            decay = 0.996

            #complex_frequency = 1j * 2 * np.pi * frequency

            pickup_index = int(electronicguitar_data["pickup_position"] * delay_int)

            num_samples = int(sound_wave_data["sampling_rate"]*sound_wave_data["duration"])
            output = np.zeros(num_samples)

            for i in range(num_samples):
                right_value = delay_line[zeroInt()]
                left_value = delay_line[oneInt()]
                new_value = decay * (right_value + left_value) / 2
                delay_line = np.roll(delay_line, -1)
                delay_line[-1] = new_value

                if pickup_index < len(delay_line) - 1:
                    pickup_signal = delay_line[pickup_index+1] - delay_line[pickup_index]
                else:
                    pickup_signal = 0.0
                
                
                #pickup_signal = self.__pickupCircuit(complex_frequency,
                                                 #electronicguitar_data["inductance"],
                                                 #electronicguitar_data["resistance"],
                                                 #electronicguitar_data["capatitance"])
                #output[i] = pickup_signal.real
                output[i] = self.__bandpassFilter(pickup_signal, sound_wave_data["sampling_rate"])
            
            output = np.tanh(output)

            #output = self.__bandpassFilter(output, sound_wave_data["sampling_rate"])

            output *= adsr_envelop

            output /= np.max(np.abs(output) + 1e-9)
            
            self.soundsInstrumentPlay.append(output)
    
    def __bandpassFilter(self, pickup_signal, sample_rate):
        """
        出力信号にバンドパスフィルタをかけて、応答します
        この関数はピックアップ回路の代替関数です
        Arguments:
            output : 出力波形
            sample_rate : サンプリング周波数
        """

        lower_limit_cutoff = 100 / (sample_rate / 2)
        upper_limit_cutoff = 6000 / (sample_rate / 2)

        b, a = butter(2, [lower_limit_cutoff, upper_limit_cutoff], btype='band')
        return lfilter(b, a, [pickup_signal])
    
    def __pickupCircuit(self, complex_frequency, inductance, 
                        resistance, capacitance):
        """
        ピックアップ回路を作成し、応答します
        Arguments:
            complex_frequency : 複素周波数 s
            inductance : インダクタンス (L)
            resistance : 直流抵抗 (R)
            capacitance : 静電気容量 (C)
        """

        numerator = complex_frequency * inductance
        paragraph_one = resistance
        paragraph_two = complex_frequency * inductance
        paragraph_three = 1 / (complex_frequency * capacitance)
        denominator = paragraph_one + paragraph_two + paragraph_three

        return numerator / denominator
