#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Piano : ピアノ
ピアノの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (blueChar, blueFrequencies,
                               soundWaveData, pianoData,
                               pianoResonator)

import numpy as np

import time

class Piano(Instrument):
    """
    ピアノ
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
            1: サウンドデータ、周波数群、pianoデータを得る
            2: 弦の長さを束縛する [6.06, 6.05, 6.04, 6.03, 6.02, 6.01, 6.00]
            3: 全ての周波数に対して、以下を繰り返す
                a. 遅延線長を決定し、バッファをノイズによって初期化
                b. ハンマー模型を準備 <- これは、3:の前段階で行う
                    ハンマーを振る速さ、ハンマーの質量, 非線形ハンマーを準備
                    速さ = 初速 + 加速度*圧力を加える時間(おそらく微小)
                    加速度 = 力 / 質量
                    弦の速度 = 弦の長さ / 圧力を加える時間
                c. サウンドボードの共鳴フィルタを準備 <- これは、3:の前段階で行う
                d. 出力波形を準備
                e. サンプル数分、以下を実行する
                    e-1. ハンマーと弦の相互作用を求める
                    e-2. 遅延線アルゴリズムを用いて、新たな値を求める
                    e-3. 弦遅延線を進める
                    e-4. new_valをサウンドボードに通す
                    e-?. ペダル効果を得て、適応する
                    e-5. 出力波形に書き込む
                f. 正規化を行って、当該プロパティに束縛する
        """

        sound_wave_data = soundWaveData()
        blue_frequencies = blueFrequencies()
        piano_data = pianoData()

        resonant_data = piano_data["resonant_filters"]
        string_lengthes = piano_data["string_lengthes"]

        hammer_acceleration = piano_data["hammer_force"] / piano_data["hammer_mass"]
        hammer_velocity = 1.0 + hammer_acceleration * piano_data["force_time"]
        hammer_position = piano_data["hammer_position"]
        string_position = piano_data["string_position"]

        dt = sound_wave_data["dt"]

        resonators = []
        for r in resonant_data:
            f = pianoResonator()
            f.setSamplingRate(fs=sound_wave_data["sampling_rate"])
            f.setFrequency(r)
            f.defineOtherProperties()
            resonators.append(f)

        for a_frequency, a_string_length in zip(blue_frequencies, string_lengthes):
            delay_length = int(sound_wave_data["sampling_rate"] / a_frequency)
            delay_line = np.random.uniform(-1, 1, delay_length)

            string_velocity = a_string_length / piano_data["force_time"]

            # string_mass u = m / L よって、m = u*L
            # このuを求める
            # 2Lf = √T / u
            # 4L^2f^2 = T / u
            # 1 / 4L^2f^2 = u / T
            # u = T / 4L^2f^2
            # ここで、 T = tension, L = length, f = frequency

            u = piano_data["string_tension"] / (4 * (a_string_length**2) * (a_frequency**2))
            #print(u)

            string_mass = u * a_string_length

            output = np.zeros(sound_wave_data["num_samples"])

            for n in range(sound_wave_data["num_samples"]):
                damping = piano_data["damping"] + 0.002 * piano_data["pedal"]
                #contact_force = self.__hammerNonliearly(hammer_velocity, string_velocity)
                contact_force = self.__hartzTypeHammerModel(hammer_position, string_position,
                                                            hammer_velocity, string_velocity,
                                                            k=1e5, p=3.0)
                #print(resonated)
                #time.sleep(0.5)

                hammer_acceleration = -contact_force / piano_data["hammer_mass"]
                string_acceleration = contact_force / string_mass
                hammer_velocity += hammer_acceleration * dt
                string_velocity += string_acceleration * dt
                hammer_position += hammer_velocity * dt
                string_position += string_velocity * dt

                new_val = 0.5 * (delay_line[0] + delay_line[-1]) * damping + string_position
                delay_line = np.roll(delay_line, -1)
                delay_line[-1] = new_val

                resonated = sum(f.process(new_val) for f in resonators)
                output[n] = resonated
            
            output /= max(abs(output))
            print(output)
            self.soundsInstrumentPlay.append(output)
    
    def __hammerNonliearly(self, hammer_velocity, string_velocity):
        """
        ハンマーと弦の相互作用から、実際にハンマーが接触した際の
        力を求め、応答します。
        Arguments:
            hammer_velocity : ハンマーの速さ
            string_velocity : 弦の速さ
        """

        delta_v = hammer_velocity - string_velocity

        return (delta_v ** 3) if delta_v > 0 else 0.0 #(hammer_velocity - string_velocity)**3 

    def __hartzTypeHammerModel(self, hammer_position, string_position, 
                               hammer_velocity, string_velocity, k, p):
        """
        Hartz型のハンマー・弦接触モデルを作成し、それを応答します。
        Arguments:
            hammer_position : ハンマーを叩いた位置
            string_position : 弦が弾かれた位置
            hammer_velocity : ハンマーを振る速さ
            string_velocity : 弦の弾き速度
            k : 剛性係数
            p : 非線形指数
        Expression:
            x = hammer_position - string_position > 0 
            and
            v = hammer_velocity - string_velocity > 0
            force = k * (x**p)
        """

        x = hammer_position - string_position   
        v = hammer_velocity - string_velocity
        force = 0.0
        if x > 0 and v > 0:
            force = k * (x**p)
        return force