#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Trumpet : トランペット
トランペットの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (redChar, redFrequencies,
                               zeroInt, oneInt, twoInt,
                               soundWaveData, trumpetData)

import numpy as np

class Trumpet(Instrument):
    """
    トランペット
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
        """

        super().__init__()
        self.color = redChar()

    def makeSound(self):
        """
        演奏する音を作成する
        Target:
            1: 必要なデータを全て用意する
               (soundWaveData, trumpetData)
            2: 全ての周波数に対して以下を実行する
        """

        sound_wave_data = soundWaveData()
        trumpet_data = trumpetData()
        red_frequencies = redFrequencies()

        effective_length = max(0.1, 
                               trumpet_data["tube_length"] + trumpet_data["mp_effective_length"])
        for a_frequency in red_frequencies:
            delay = max(2, int(effective_length / sound_wave_data["sound_speed"] * a_frequency))

            right = np.zeros(delay)
            left = np.zeros(delay)
            output = np.zeros(sound_wave_data["num_samples"])
            x = 0.0
            v = 0.0
            k = (2 * np.pi * a_frequency)**2

            tube_area = trumpet_data["mouse_open_area_scale"]
            Zc = trumpet_data["rho"] * sound_wave_data["sound_speed"] / tube_area

            for n in range(sound_wave_data["num_samples"]):
                Pc = right[0] + left[0]
                dp = trumpet_data["blowing_pressure"] - Pc
                A = max(0.0, trumpet_data["a0"] + trumpet_data["a1"] * x + trumpet_data["a2"] * x * x)
                accel = (dp * A - trumpet_data["damping"] * v - k * x)
                v += accel * sound_wave_data["dt"]
                x+= v * sound_wave_data["dt"]
                U = A * np.sign(dp) * np.sqrt(2.0 * abs(dp) / trumpet_data["rho"])
                if trumpet_data["use_impedance_conversion"] == True:
                    inject_p = U * Zc
                else:
                    inject_p = trumpet_data["Z_scale"] * U
                inject_p *= trumpet_data["injected_scale"]

                right = np.roll(right, 1)
                left = np.roll(left, -1)

                right[0] = trumpet_data["r_mouth"] * left[0] + inject_p
                left[-1] = right[-1]
                output[n] = Pc
            
            maxv = np.max(np.abs(output)) + 1e-12
            output = output / maxv * 0.95
            self.soundsInstrumentPlay.append(output)
        