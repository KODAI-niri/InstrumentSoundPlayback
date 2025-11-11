#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Violinのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Violin import Violin

import sounddevice as sd

import time

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:44 音が割れている。
    """

    violin = Violin()
    violin.makeSound()

    sounds = violin.getSoundsInstrumentPlay()

    for sound in sounds:
        print(sound)
        #sd.play(sound)
        #sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())