#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Violin: ヴァイオリン
ヴァイオリンの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (greenChar, greenFrequencies,
                               soundWaveData, violinData)

import numpy as np

import math

class Violin(Instrument):
    """
    ヴァイオリン
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
        Target:
            1: サウンドデータやヴァイオリンデータ、周波数を得る
            2: 全ての周波数に対して、以下を実行する
                a. 弦の張力を考慮した周波数を求め、遅延線を求める
                b. 出力配列をゼロで初期化する
                c. 弓の状態(弓が引いている弦の位置)を初期化する
                d. 出力配列の大きさ分、以下を実行する
                    d-1. 弓と弦の相対速度を求める
                    d_2. 摩擦による力を摩擦モデルから求める
                    (摩擦モデル) = (0.5 + 0.5 * string_tension) * 摩擦モデル(v_relative, bow_pressure)
                    d_3. reclrection_coeffを更新する(ちなしなくても良い)
                    d_4. 力を元に加える
                    d_5. 出力を行う(つまり、output[n]に伝播した遅延線を束縛させる)
                e. 正規化を行う
                f. 右耳成分を再現する
                g. 自分自身が持つ当該プロパティに出力波形を束縛させる
        """

        green_frequencies = greenFrequencies()
        sound_wave_data   = soundWaveData()
        violin_data       = violinData()

        for a_frequency in green_frequencies:
            effective_freq = a_frequency * violin_data["string_tension"]
            delay_len = int(sound_wave_data["num_samples"] / effective_freq)
            delay_line = np.zeros(delay_len)

            output = np.zeros(sound_wave_data["num_samples"])

            bow_position = delay_len // 3

            for n in range(sound_wave_data["num_samples"]):
                v_bow = violin_data["bow_velocity"]
                v_string = delay_line[bow_position]
                v_rel = v_bow - v_string

                force = self.__friction_force(v_rel, violin_data["bow_pressure"])
                force *= (0.5 + 0.5 * violin_data["string_tension"])

                delay_line[0] = force + violin_data["reflection_coeff"] * delay_line[-1]
                delay_line = np.roll(delay_line, -1)
                output[n] = delay_line[-1] * violin_data["damping"]
            
            output /= max(abs(output))

            self.soundsInstrumentPlay.append(output)
    
    def __friction_force(self, v_relative, pressure):
        """
        摩擦モデル: 非線形摩擦特性を近似し、応答します
        Arguments:
            v_relative : 弓と弦の相対速度
            pressure : 弓による摩擦力
        """

        return math.tanh(-v_relative * pressure * 5.0)
