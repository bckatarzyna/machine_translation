def prepare_sentences (e_sentences, f_sentences):
    f_sentences = [ f.lower().split() for f in f_sentences ]
    e_sentences = [ e.lower().split() for e in e_sentences ]
    return e_sentences, f_sentences

def load_sentences (e_file, f_file):
    with open(f_file) as source, open(e_file) as target:
        e_file = [ line for line in target ]
        f_file = [ line for line in source ]
    e_sentences, f_sentences = prepare_sentences(e_file, f_file)
    return e_sentences, f_sentences

def split_into_pairs(pair_list):
    pairs = []
    for pair in pair_list:
        pairs.append((pair.split('-')[0], pair.split('-')[1]))
    return pairs

def load_alignment (a_file):
    with open(a_file) as alignment:
        a = [ line for line in alignment ]
        a = [ a_item.split() for a_item in a ]
        a = [ split_into_pairs(a_item) for a_item in a ]
    return a
