from collections import defaultdict
from preprocessing import load_sentences, load_alignment

def aligned(A, f_ind, e_start, e_end):
    f_aligned = []
    for pair in A:
        e, f = int(pair[0]), int(pair[1])
        if f == f_ind:
            f_aligned.append(e)
    if len(f_aligned) > 0 and (min(f_aligned) < e_start or max(f_aligned) > e_end):
        return False
    return True


def extract (A, f_start, f_end, e_start, e_end, e_sent, f_sent):
    E = set()
    
    if f_end == 0:
        return E    
    for pair in A:
        e, f = int(pair[0]), int(pair[1])
        if f_start <= f and f <= f_end and (e < e_start or e > e_end):
            return E
        
    f_s = f_start
    while True:
        f_e = f_end
        while True:
            e_phrase = ""
            f_phrase = ""
            for i in range(e_start, e_end + 1):
                e_phrase += e_sent[i - 1] + " "
            for i in range(f_s, f_e + 1):
                f_phrase += f_sent[i - 1] + " "
            phrases_pair = (e_phrase, f_phrase)
            E.add(phrases_pair)
            f_e += 1
            if f_e > len(f_sent) or not aligned(A, f_e, e_start, e_end):
                break
        f_s -= 1
        if f_s < 1 or not aligned(A, f_s, e_start, e_end):
            break
    
    return E


def phrase_extraction (e_file, f_file, alignment): 
    e_list, f_list = load_sentences(e_file, f_file)
    A = load_alignment(alignment)
    BP = set()
    
    for i in range(len(e_list)):
        for e_start in range(1, len(e_list[i]) + 1):
            for e_end in range(e_start, len(e_list[i]) + 1):
                f_start, f_end = len(f_list[i]), 0
                for pair in A[i]:
                    e, f = int(pair[0]), int(pair[1])
                    if e_start <= e and e <= e_end:
                        f_start = min(f, f_start)
                        f_end = max(f, f_end)
                new_phrases = extract(A[i], f_start, f_end, e_start, e_end, e_list[i], f_list[i])
                for phrase in new_phrases:
                    BP.add(phrase)
                       
    return BP
