#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Trumpetのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Trumpet import Trumpet

import sounddevice as sd

import time

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:38 何もされることなく一瞬で終わる
    """

    trumpet = Trumpet()
    trumpet.makeSound()

    sounds = trumpet.getSoundsInstrumentPlay()

    for sound in sounds:
        #print(sound)
        sd.play(sound)
        sd.wait(3.0)

if __name__ == '__main__':
    import sys

    sys.exit(main())