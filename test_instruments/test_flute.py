#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Fluteのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Flute import Flute

import sounddevice as sd

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している
    
    テスト結果:
        10/30 11:05 全部ザーザー音で草
        11/1  12:23 息が強め?なのかな?
    """

    flute = Flute()
    flute.makeSound()

    sounds = flute.getSoundsInstrumentPlay()

    for sound in sounds:
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())