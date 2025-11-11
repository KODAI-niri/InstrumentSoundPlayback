#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Color : Blue,Green,Red,Yellowの
親クラスであるクラスを定義するファイル
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24 (Updated: 2025/11/11)" 

from Instrument.Instrument import Instrument

class Color:
    """
    Colorクラス
    Goal:
        Blue,Green,Red,Yellowの親となる
        クラスを正しく定義すること
    Target:
        0:  まずは、楽器クラスを全て作成し、正しく動作することを証明する
        1:  __init__の作成
        2:  prepareToPerformの作成
        2:  performの作成
        3:  テスト(いらんかも)を行う
    Properties:
        instruments: 音を出す楽器群
    """

    def __init__(self):
        """
        このクラスのコンストラクタ
        instrumentsプロパティを初期化する
        """

        self.instruments = []
    
    def prepareToPerform(self):
        """
        演奏(音を出す)ための準備を行います。
        自分が持っている楽器それぞれのmakeSoundを呼び出します
        """

        for an_instrument in self.instruments:
            assert isinstance(an_instrument, Instrument)
            an_instrument.makeSound()
    
    def perform(self):
        """
        演奏を行います。
        Targets:
            1. それぞれの楽器に対して以下を実行する
                a. 楽器の音を得る
                b. 全ての楽器の音に対して、以下を繰り返す
                    b_1. 音を鳴らす(sd.play(sound))
                    b_2. 音が鳴り終わるまで待つ
        但し、このperformは何もしない。子クラスのperformに処理を任せる
        """

        pass