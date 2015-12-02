from itertools import chain
from collections import defaultdict
from decimal import *
import math
import operator

def load_sentences (f_file, e_file):
    with open(f_file) as source, open(e_file) as target:
        f_file = [ line for line in source ]
        e_file = [ line for line in target ]
    return f_file, e_file

def prepare_sentences (f_sentences, e_sentences):
    f_sentences = [ f.lower().split() + ['NULL'] for f in f_sentences ]
    e_sentences = [ e.lower().split() for e in e_sentences ]
    return f_sentences, e_sentences

def perplexity (t, target):
    probabilities = [] 
    for target_sent in target:
        probs = 1.0
        for t_word in target_sent:
            probs *= max(t[t_word].iteritems(), key=operator.itemgetter(1))[1]
        probabilities.append(math.log(probs, 2))
    return 2**Decimal(-sum(probabilities))

def model1 (source_file, target_file, iterations, convergence):
    
    # loading data
    source, target = load_sentences(source_file, target_file)
    source, target = prepare_sentences(source, target)
    
    flattened_source = [item for sublist in source for item in sublist]
    flattened_target = [item for sublist in target for item in sublist]
        
    all_source_words = frozenset(flattened_source)
    all_target_words = frozenset(flattened_target)
    
    # initialize t uniformly
    t = {t_word: {s_word: 0.5 for s_word in all_source_words} for t_word in all_target_words}
    
    old_perp = 10**15
    perp = 10**14
    i = 0
    while ((iterations != None and i < iterations) or (convergence != None and (old_perp - perp) > convergence)):
#    for i in range(iterations):

        # initializing count, total and s_total
        count = {t_word: {s_word: 0.0 for s_word in all_source_words} for t_word in all_target_words}
        total = defaultdict(float)
        s_total = defaultdict(float)
        
        for source_sent, target_sent in zip(source, target):
            # compute normalization
            for t_word in target_sent:
                s_total[t_word] = 0
                for s_word in source_sent:
                    s_total[t_word] += t[t_word][s_word]
            
            #collect counts
            for t_word in target_sent:
                for s_word in source_sent:
                    count[t_word][s_word] += t[t_word][s_word] / s_total[t_word]
                    total[s_word] += t[t_word][s_word] / s_total[t_word]
                    
        # estimate probabilities
        for s_word in all_source_words:
            for t_word in all_target_words:
                t[t_word][s_word] = count[t_word][s_word] / total[s_word]
        
	i = i + 1
	old_perp = perp
	perp = perplexity(t, target)
	print 'iterations: ', i
	print perp

    return t, perp
