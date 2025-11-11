#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
JapaneseGuitarのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.JapaneseGuitar import JapaneseGuitar

import sounddevice as sd

import time

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:11 何も音が鳴らない!! なんで?? -> 音が小さすぎてなってない
        10/30 11:18 いい感じに音が鳴った!!
    """

    japanese_guitar = JapaneseGuitar()
    japanese_guitar.makeSound()

    sounds = japanese_guitar.getSoundsInstrumentPlay()

    for sound in sounds:
        #print(sound)
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())