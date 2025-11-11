#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Ukuleleのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Ukulele import Ukulele

import sounddevice as sd

import time

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:40 まあまあの音かな 実音と比べる
    """

    ukulele = Ukulele()
    ukulele.makeSound()

    sounds = ukulele.getSoundsInstrumentPlay()

    for sound in sounds:
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys
    
    sys.exit(main())