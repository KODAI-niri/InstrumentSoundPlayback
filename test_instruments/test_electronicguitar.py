#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
ElectronicGuitarのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.ElectronicGuitar import ElectronicGuitar

import sounddevice as sd

from scipy.io.wavfile import write

import os

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:04 -> 三味線のような音 ギター感がない。電子感もない
        10/30 12:27 -> 残響が減って、電子的な感じに近づく
    """

    electronic_guitar = ElectronicGuitar()
    electronic_guitar.makeSound()

    sounds = electronic_guitar.getSoundsInstrumentPlay()

    for sound in sounds:
        #print(sound)
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys
    
    sys.exit(main())
