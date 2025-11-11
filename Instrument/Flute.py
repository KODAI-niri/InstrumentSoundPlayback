#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Flute : フルート
フルートの音を再現するクラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from .Instrument import Instrument

from Returner.Returner import (greenChar, greenFrequencies,
                               soundWaveData, fluteData)

import numpy as np

class Flute(Instrument):
    """
    フルート
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
        スーパークラスのコンストラクタを呼び出し、
        自身が属する色を束縛しておく
        """

        super().__init__()
        self.color = greenChar()
    
    def makeSound(self):
        """
        奏でる音を作成する
        """

        sound_wave_data = soundWaveData()
        flute_data = fluteData()
        green_frequencies = greenFrequencies()

        for a_frequency in green_frequencies:
            pipe_length = sound_wave_data["sound_speed"] / (2 * a_frequency)

            delay_length = int(sound_wave_data["sampling_rate"] * 2 * pipe_length / sound_wave_data["sound_speed"])

            right_buffer = np.zeros(delay_length)
            left_buffer = np.zeros(delay_length)  

            jet_state = 0.0
            jet_delay_samples = int(flute_data["jet_delay"]*delay_length)

            jet_delay = np.zeros(jet_delay_samples)

            output = np.zeros(sound_wave_data["num_samples"])

            for n in range(sound_wave_data["num_samples"]):
                pressure_in = flute_data["blowing_pressure"] + flute_data["noise_level"] * np.random.randn()

                p_reflected = left_buffer[-1]

                jet_input = pressure_in - jet_state

                jet_delay = np.roll(jet_delay, -1)
                jet_delay[0] = jet_input

                # implement jet oscillation in half space
                # jet_output = self.__jetOscillationInHalfSpace(jet_delay, a_frequency)

                # implement proposed jet oscillation
                jet_output = self.__proposedJetOscillation(jet_delay, a_frequency)

                #jet_output = np.tanh(jet_input * 5.0)

                left_buffer = np.roll(left_buffer, -1)
                right_buffer = np.roll(right_buffer, 1)

                right_buffer[0] = jet_output + p_reflected * flute_data["damping"]
                left_buffer[-1] = -right_buffer[-1]

                output[n] = right_buffer[-1]
            
            #output += flute_data["noise_level"] * np.random.rand(len(output))

            output /= max(abs(output))

            self.soundsInstrumentPlay.append(output)
    
    def __jetOscillationInHalfSpace(self, x, frequency):
        """
        半空間におけるjetモデルを作成し、応答します
        Arguments:
            x : jet_input 
            frequency : 周波数
        Return:
            jet(x).real ジェットモデルの最大振幅の実部(型が合わないため)
        """

        c_p = 5
        u = 0.01

        complex_frequency = 1j * 2 * np.pi * frequency

        first_expression = u - (complex_frequency / c_p)
        second_expression = x * first_expression
        exp = np.exp(second_expression)
        third_expression = 1 - exp
        real_values = third_expression.real
        function_y = sorted(real_values, reverse=True)[0]

        return function_y
    
    def __proposedJetOscillation(self, x, frequency):
        """
        Jet oscillation model for flute-like instruments 
        allowing overall deflection(January 10 2024)で提案された
        jetモデルを作成し、応答します。
        Arguments:
            x : jet_input
            frequency : 周波数
        Expression:
            ηα(x) : eta = YW[3α(x/W)^2 + r(1 - exp(µx-iωx/cp))]
            α =  self.__alphaForJet
            r = 0.9 or 0.1
            µ = 0.01
            cp = 5
            W = 0.05
            ω = 1j * 2 * π(np.pi or math.pi) * frequency
        Return:
            jet(x).real ジェットモデルの最大振幅の実部
        """ 

        c_p = 5
        u = 0.01
        omega = 1j * 2 * np.pi * frequency
        r_coeff = 0.9
        W = 0.05
        alpha_for_jet = self.__alphaForJet(c_p, omega, r_coeff, u, W)

        index = x * (u - (omega / c_p))

        eta_parag_one = 3 * alpha_for_jet * np.square(x/W)
        eta_parag_two = r_coeff * (1 - np.exp(index))
        eta = eta_parag_one + eta_parag_two
        eta_reals = eta.real
        function_y = sorted(eta_reals, reverse=True)[0]
        return function_y

    
    def __alphaForJet(self, c_p, omega, r_coeff, u, W):
        """
        jetモデルのα係数を求め、それを応答します
        Arguments:
            c_p : ジェット擾乱の伝播速度
            omega : 角周波数 2πf
            r_coeff : 反射率
            u : ジェット不安定性の成長率
            W : ノズルから口縁までの距離
        Expression:
            α = 1 + r(1 - ((1 - exp(u*W-omega*W/c_p)) / u*W-omega*W/c_p))
        Return:
            α係数 for Jet Model
        """

        ffr_parag_one = 1
        ffr_parag_two = (1 - np.exp(u*W-omega*W/c_p)) / (u*W-omega*W/c_p)
        formula_for_r = ffr_parag_one + ffr_parag_two
        alpha_parag_two = r_coeff * formula_for_r
        return 1 + alpha_parag_two