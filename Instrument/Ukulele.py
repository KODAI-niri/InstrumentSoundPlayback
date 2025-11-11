#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Ukulele : ウクレレ
ウクレレの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/26"

from .Instrument import Instrument

from Returner.Returner import (yellowChar, yellowFrequencies,
                               soundWaveData, ukuleleData,
                               ukuleleADSREnvelopTimeData)

import numpy as np

from scipy.signal import lfilter

from collections import deque

class Ukulele(Instrument):
    """
    ウクレレクラス
    Goal:
        黄色の周波数 = 
        [554.36, 587.33, 622.25, 647, 659.25, 698.45, 739.98]
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
        """

        super().__init__()
        self.color = yellowChar()
    
    def makeSound(self):
        """
        奏でる音を作成する
        """

        sound_wave_data = soundWaveData()
        yellow_frequencies = yellowFrequencies()
        ukulele_data = ukuleleData()
        ukulele_envelop = ukuleleADSREnvelopTimeData()

        for a_frequency in yellow_frequencies:
            delay_length = sound_wave_data["sampling_rate"] / a_frequency
            delay_line = self.__create_initial_wave(ukulele_data["pluck_force"],
                                                    ukulele_data["pluck_position"],
                                                    delay_length)
            
            output = np.zeros(sound_wave_data["num_samples"])

            for n in range(sound_wave_data["num_samples"]):
                y = ukulele_data["damping"] * ((delay_line[0] + delay_line[1]) / 2)
                delay_line.append(y)
                delay_line.popleft()
                output[n] = y

            for a_body in ukulele_data["body_resonance"]:
                output = self.__resonant_filter(output, a_body)
                
            output *= ukulele_envelop

            output /= max(abs(output))

            self.soundsInstrumentPlay.append(output)
            
    def __create_initial_wave(self, pluck_force, pluck_position, delay_length):
        """
        初期波形を求めて、応答します
        Arguments:
            pluck_force : 弦を弾く強さ
            pluck_position : 弦を弾く位置
            delay_length : 遅延線の長さ
        """

        L = int(delay_length)
        Np = int(L * pluck_position)
        wave = np.zeros(L)
        for i in range(L):
            if i < Np:
                wave[i] = (pluck_force / Np) * i
            else:
                wave[i] = pluck_force * (1 - (i - Np) / (L - Np))
        return deque(wave)
    
    def __resonant_filter(self, output, frequency, Q=5, sample_rate=44100):
        """
        出力波形にIIRフィルターを掛けます。
        Arguments:
            output : 出力波形
            frequency : 周波数
            Q : ?
        """

        omega = 2 * np.pi * frequency / sample_rate
        alpha = np.sin(omega) / (2 * Q)

        b0 = alpha
        b1 = 0
        b2 = -alpha
        a0 = 1 + alpha
        a1 = -2 * np.cos(omega)
        a2 = 1 - alpha

        b = np.array([b0, b1, b2]) / a0
        a = np.array([1, a1 / a0, a2 / a0])
        return lfilter(b, a, output)