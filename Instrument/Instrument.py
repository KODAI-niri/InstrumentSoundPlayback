#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Instrument : 楽器という抽象的な表現
すべての楽器が継承する最も(抽象的な)
親クラス
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24"

from Returner.Returner import *

class Instrument:
    """
    すべての楽器の親クラス
    Goal:
        子クラスが継承する準備を整える
        つまり、プロパティやメソッドを完成させること
    Target:
        1: __init__を完成させる プロパティを初期化する(ゲッターも用意)
        2: makeSoundを実装、といってもこのクラスのmakeSoundはpass
    """

    def __init__(self):
        """
        このクラスのコンストラクタ
        この楽器が奏でる音の群れプロパティと
        所属する色(文字列)のプロパティを初期化する
        """

        self.soundsInstrumentPlay = emptyList()
        self.color = blankChar()
    
    def makeSound(self):
        """
        pass method
        """

        pass

    def getSoundsInstrumentPlay(self):
        """
        楽器が演奏する音の集合を応答します
        """

        return self.soundsInstrumentPlay
