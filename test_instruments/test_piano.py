#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
Pianoのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.Piano import Piano

import sounddevice as sd

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している

    テスト結果:
        10/30 11:23
        /Users/nyx_z/AP/MyPythonProgramming/sonification/InstrumentSoundPlayback/Instrument/Piano.py:106: RuntimeWarning: invalid value encountered in divide
        output /= max(abs(output))
        追記11/1 ハンマー模型が全て0を応答していることが原因。より良いモデルを探すことが求められる
    """

    piano = Piano()
    piano.makeSound()

    sounds = piano.getSoundsInstrumentPlay()

    for sound in sounds:
        sd.play(sound)
        sd.wait(3.0)

    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())