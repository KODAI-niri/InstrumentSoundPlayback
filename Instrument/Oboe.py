#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Oboe : オーボエ
オーボエの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (redChar, redFrequencies,
                               soundWaveData, returnTimeData,
                               oboeData, zeroInt, oneInt, twoInt)

import numpy as np

class Oboe(Instrument):
    """
    オーボエ
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
        奏でる音を作成する
        1: 必要なデータ(周波数群、サウンドデータ、オーボエデータ)を得る
        2: 全ての周波数に対して、以下を実行する
           delay_lengthを求め、outputとright_wave, left_waveを0で初期化
           2-: サンプル数に対して、以下を実行する
            a. p_bとp_cを求め、delta_pを求める
            b. UとZ0を求め、新しい右向き波を求める
            c. right_waveとleft_waveを一つロールする
            d. right_waveの先頭を新しい波で更新する
            e. 右向き波を反転させ、反射波を得る
            f. output[n]を更新する
        """

        sound_wave_data = soundWaveData()
        oboe_data = oboeData()
        red_frequencies = redFrequencies()

        for a_frequency in red_frequencies:
            delay_length = int(sound_wave_data["sampling_rate"] / (twoInt() * a_frequency))
            output = np.zeros(sound_wave_data["num_samples"])
            right_wave = np.zeros(delay_length)
            left_wave = np.zeros(delay_length)

            for n in range(sound_wave_data["num_samples"]):
                p_b = oboe_data["blowing_pressure"] * (1.0 + 0.005 * np.sin(2 * np.pi * 5 * n / sound_wave_data["sampling_rate"]))
                p_c = right_wave[zeroInt()] + left_wave[zeroInt()]
                #print(p_c)
                delta_p = p_b - p_c
                if delta_p > oboe_data["threshold"]:
                    U = max(zeroInt(), oboe_data["alpha"]*(delta_p - oboe_data["threshold"]))
                else:
                    U = 0.0
                print(U)
                Z0 = sound_wave_data["sound_speed"] * oboe_data["rho"]

                p_plus_new = left_wave[zeroInt()] + (Z0 * U / twoInt())

                right_wave[zeroInt()] = p_plus_new
                right_wave = np.roll(right_wave, oneInt())
                left_wave = np.roll(left_wave, -oneInt())
                left_wave[-1] = oboe_data["reflection"] * right_wave[-1]
                output[n] = right_wave[-1] + left_wave[-1]
            
            #print(left_wave)
            #print(right_wave)
            #print(output)
            output /= max(abs(output))
            #print(output[0:1000])
        
            self.soundsInstrumentPlay.append(output)