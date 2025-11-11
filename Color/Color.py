#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Color : Blue,Green,Red,Yellowの
親クラスであるクラスを定義するファイル
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/24 (Updated: 2025/11/11)" 

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