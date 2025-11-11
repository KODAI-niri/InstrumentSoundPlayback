#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Oboeのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Oboe import Oboe

import sounddevice as sd

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:22
        /Users/nyx_z/AP/MyPythonProgramming/sonification/InstrumentSoundPlayback/Instrument/Oboe.py:84: RuntimeWarning: invalid value encountered in divide
        output /= max(abs(output))
        11/1 16:41
        バグ直る 正しい音が出ているかどうかは不明
    """

    oboe = Oboe()
    oboe.makeSound()

    sounds = oboe.getSoundsInstrumentPlay()

    for sound in sounds:
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())
