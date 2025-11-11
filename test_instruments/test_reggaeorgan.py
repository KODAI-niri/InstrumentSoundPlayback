#! /usr/bin/env python
#! -*- coding: utf-8 -*-

"""
ReggeOrganのテストを行うプログラム
"""

__author__ = "Tsuji Kodai"
__version__ = "1.0.0"
__date__ = "2025/10/29"

from Instrument.ReggaeOrgan import ReggaeOrgan

import sounddevice as sd

import time

def main():
    """
    テストのメインプログラム
    常にリターンコードが0となることを想定している
    
    テスト結果:
        10:/30 11:41 まあまあの音 実音と比べる
    """

    regaae_organ = ReggaeOrgan()
    regaae_organ.makeSound()

    sounds = regaae_organ.getSoundsInstrumentPlay()

    for sound in sounds:
        sd.play(sound)
        sd.wait(3.0)
    
    return 0

if __name__ == '__main__':
    import sys

    sys.exit(main())