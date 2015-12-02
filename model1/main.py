#!/usr/bin/env python
import argparse
from model1 import model1

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="IBM Model 1")
    parser.add_argument('source_file', type=str)
    parser.add_argument('target_file', type=str)
    parser.add_argument('-i', '--iterations', type=int)
    parser.add_argument('-c', '--convergence', type=float)
    args = parser.parse_args()
    
    t, perplexity = model1(args.source_file, args.target_file, args.iterations, args.convergence)

    for e, f_words in t.iteritems():
        for f, prob in f_words.iteritems():
            if prob >= 0.0001:
                print "%s    %s    %.4f" % (f, e, prob)

    print "perplexity: %.4f" % (perplexity)

