#!/usr/bin/env python
import argparse
from phrase_extraction import phrase_extraction

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="Phrase extraction")
    parser.add_argument('f_file', type=str)
    parser.add_argument('e_file', type=str)
    parser.add_argument('alignment', type=str)
    args = parser.parse_args()
    
    phrases = phrase_extraction(args.e_file, args.f_file, args.alignment)

    for phrase in phrases:
        print phrase[0], ' - ', phrase[1]


