#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
JapanaseGuitar : 三味線
三味線の音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (greenChar, greenFrequencies,
                               soundWaveData, japaneseGuitarData)

import numpy as np

from scipy.signal import lfilter

from collections import deque

class JapaneseGuitar(Instrument):
    """
    三味線
    Goal:
        緑色の周波数 = 
        [349.23, 370.00, 392.00, 408, 415.31, 440.01, 466.17]
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
        self.color = greenChar()
    
    def makeSound(self):
        """
        奏でる音を作成する
        """

        sound_wave_data = soundWaveData()
        green_frequencies = greenFrequencies()
        japanese_guitar_data = japaneseGuitarData()

        for a_frequency in green_frequencies:
            delay_length = int(sound_wave_data["sampling_rate"] / a_frequency)

            buffer = self.__create_initialized_noise(japanese_guitar_data["pick_force"],
                                                     japanese_guitar_data["pick_position"],
                                                     delay_length)
            
            buffer = self.__pick_position_filter(buffer, 
                                                 japanese_guitar_data["pick_position"],
                                                 delay_length)
            
            output = np.zeros(sound_wave_data["num_samples"])

            for n in range(sound_wave_data["num_samples"]):
                x0 = buffer[0]
                x1 = buffer[1]
                averaged = 0.5 * (x0 + x1)
                new_val = averaged * japanese_guitar_data["damping"]
                buffer = np.roll(buffer, -1)
                buffer[-1] = new_val
                output[n] = new_val

            for mode in japanese_guitar_data["body_modes"]:
                output = self.__resonant_filter(output, mode)
            
            output /= max(abs(output))
            self.soundsInstrumentPlay.append(output)
            
    
    def __create_initialized_noise(self, 
                                   pick_force,
                                   pick_position,
                                   delay_length):
        """
        初期ノイズを作成する
        Arguments:
            pick_force : 弾く強さ
            pick_position : 弾く位置
            delay_length : ノイズ信号の長さ
        """

        noise = np.random.uniform(-1, 1, delay_length)

        position = int(pick_position * delay_length)
        window = np.hanning(delay_length)
        window = np.roll(window, position)
        windowed_random = noise * window * pick_force

        return windowed_random
    
    def __pick_position_filter(self, buffer, pick_position, delay_length):
        """
        特定の周波数を打ち消すフィルターをバッファにかけて、
        応答します
        Arguments:
            buffer : バッファ
            pick_position : 弾く位置
            delay_length : ノイズ信号の長さ
        """

        delay = int(pick_position * delay_length)
        if delay == 0:
            return buffer
        filtered = np.copy(buffer)
        for i in range(delay, len(buffer)):
            filtered[i] -= buffer[i - delay]
        return filtered

    def __resonant_filter(self, output, frequency, Q=4, sample_rate=44100):
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