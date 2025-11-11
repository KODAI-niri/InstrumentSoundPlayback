#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
ReggaeOrgan : レゲエオルガン
レゲエオルガンの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (redChar, redFrequencies,
                               soundWaveData, reggaeADSREnvelopTimeData,
                               zeroInt, oneInt, twoInt,
                               returnFalse, returnReggaeHarmonics,
                               returnReggaeAmplitude, returnTimeData)

import numpy as np

class ReggaeOrgan(Instrument):
    """
    ピアノ
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
        奏でる音を作成します
        Target:
            1. 時間軸配列tを生成
            2. 全ての周波数に対して、以下を実行 -> a_frequency
                出力波形を0で初期化
                各倍音について、
                    a. 求める周波数 = a_frequency * harmonics[i]
                    b. 正弦波 = sin(2π * 周波数 * t)
                    c. 振幅 = amplitudes[i]
                    d. 出力波形に足し合わせる
                エンベロープを適用する
                波形を正規化する
                正規化した波形を束縛する
        """

        sound_wave_data = soundWaveData()
        red_frequencies = redFrequencies()
        harmonics = returnReggaeHarmonics()
        amplitudes = returnReggaeAmplitude()
        num_samples = int(sound_wave_data["duration"]*sound_wave_data["sampling_rate"])
        t = returnTimeData()
        adsr_envelop = reggaeADSREnvelopTimeData()
        for a_frequency in red_frequencies:
            output = np.zeros(num_samples)
            for a_harmonic, an_amplitude in zip(harmonics, amplitudes):
                f = a_frequency * a_harmonic
                sin_wave = np.sin(2 * np.pi * f * t)
                wave = sin_wave * an_amplitude
                output += wave
            output *= adsr_envelop
            output /= np.max(output)
            self.soundsInstrumentPlay.append(output)
