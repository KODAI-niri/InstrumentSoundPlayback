#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Vibraphone : ヴィブラフォン
ヴィブラフォンの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/27"

from .Instrument import Instrument

from Returner.Returner import (blueChar, blueFrequencies,
                               soundWaveData, vibraphoneData,
                               returnTimeData)

import numpy as np

class Vibraphone(Instrument):
    """
    ヴィブラフォン
    Goal:
        青色の周波数 = 
        [220.00, 233.08, 246.94, 256, 261.62, 277.178, 293.66]
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
        self.color = blueChar()
    
    def makeSound(self):
        """
        奏でる音を作成する
        Target:
            1: サウンドデータ、周波数群、Vibraphoneデータを得る
            2: 時間軸データtを束縛する
            3: 共鳴モードの周波数比を束縛する
            4: 全ての周波数に対して、以下を繰り返す
                a. 各モードの周波数と周波数に対する重み付けを得る
                b. 各モードごとに遅延線を初期化(uniform(-1, 1) * mallet_force)
                c. 出力バッファを確保
                d. サンプル数に対して、以下を実行
                    d-1. ファン回転によるビブラートを周波数に掛ける
                    d-2. 各モードの遅延線を1ステップ進め、加算
                    d-3. 出力波形に記録をする
                e. 出力を正規化し、当該プロパティに加える
        """

        sound_wave_data = soundWaveData()
        blue_frequencies = blueFrequencies()
        vibraphone_data = vibraphoneData()
        time_data = returnTimeData()

        vibrato_depth = vibraphone_data["vibrato_depth"]
        vibrato_rate = vibraphone_data["vibrato_rate"]

        reso_mode_freq_ratios = vibraphone_data["f_n"]

        for frequency in blue_frequencies:
            #effective_freq = frequency * reso_mode_freq_ratios[i]
            #mode_weight = self.__mode_weight(reso_mode_freq_ratios[i],
            #                                 vibraphone_data["strike_position"],
            #                                 vibraphone_data["mallet_size"])
            #delay_length = sound_wave_data["sampling_rate"] / effective_freq
            #delay_line = np.random.uniform(-1, 1, delay_length)

            output = np.zeros(sound_wave_data["num_samples"])

            for i, ratio in enumerate(reso_mode_freq_ratios):
                effective_freq = frequency * ratio
                delay_length = int(sound_wave_data["sampling_rate"] / effective_freq)
                delay_line = np.random.uniform(-1, 1, delay_length)
                weight = self.__mode_weight(ratio,
                                            vibraphone_data["strike_position"],
                                            vibraphone_data["mallet_size"])
                
                for n in range(sound_wave_data["num_samples"]):
                    vibrato = 1.0 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * time_data[n])
                    damping = vibraphone_data["damping"]**(1 + i*0.1)
                    val = 0.5 * (delay_line[0] + delay_line[1]) * damping * vibrato
                    output[n] += val * weight
                    delay_line = np.roll(delay_line, -1)
                    delay_line[-1] = val

            #for n in range(sound_wave_data["num_samples"]):
            #    vibrato = 1.0 + vibrato_depth * np.sin(2 * np.pi * vibrato_rate * time_data)

            #    mode_sum = 0
            #    for a_mode in reso_mode_freq_ratios:
            #        val = vibraphone_data["damping"] * vibrato
            #        mode_sum += val * mode_weight
                
            #    delay_line[0] = mode_sum * delay_line[-1]
            #    delay_line = np.roll(delay_line, -1)
            #    output[n] = delay_line[-1]
            
            output /= max(abs(output))

            self.soundsInstrumentPlay.append(output)
    
    def __mode_weight(self, f_n, strike_position, mallet_size):
        """
        共鳴モードの重みを応答します
        Arguments:
            f_n : 比率
            strike_position : 打撃位置
            mallet_size : マレットサイズ
        """

        pos_factor = np.sin(np.pi * f_n * strike_position)
        mallet_factor = np.exp(- (mallet_size * f_n)**2)
        return pos_factor * mallet_factor