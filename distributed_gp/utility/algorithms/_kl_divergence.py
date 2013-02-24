import re, math, collections

def tokenize(_str, n_gram = 5):
    _str = _str.lower()
    #n_gram here
    _str_size = len(_str)
    tokens = collections.defaultdict(lambda: 0.)


    # find the n_gram
    for i in range(0, _str_size - n_gram):
        tokens[ _str[i:i+n_gram] ] += 1
    return tokens
    
    # find the words intead of n_gram
    stopwords = ['and', 'for', 'if', 'the', 'then', 'be', 'is', 'are', 'will', 'in', 'it', 'to', 'that']
    tokens = collections.defaultdict(lambda: 0.)
    for m in re.finditer(r"(\w+)", _str, re.UNICODE):
        m = m.group(1).lower()
        if len(m) < 2: continue
        if m in stopwords: continue
        tokens[m] += 1

    return tokens
#end of tokenize

def kldiv(_s, _t):
    if (len(_s) == 0):
        return None

    if (len(_t) == 0):
        return None

    ssum = 0. + sum(_s.values())
    slen = len(_s)

    tsum = 0. + sum(_t.values())
    tlen = len(_t)

    vocabdiff = set(_s.keys()).difference(set(_t.keys()))
    lenvocabdiff = len(vocabdiff)

    """ epsilon """
    epsilon = min(min(_s.values())/ssum, min(_t.values())/tsum) * 0.001

    """ gamma """
    gamma = 1 - lenvocabdiff * epsilon

    # print "_s: %s" % _s
    # print "_t: %s" % _t

    """ Check if distribution probabilities sum to 1"""
    sc = sum([v/ssum for v in _s.itervalues()])
    st = sum([v/tsum for v in _t.itervalues()])

    if sc < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: sc does not sum up to 1. Bailing out .."
        sys.exit(2)
    if st < 9e-6:
        print "Sum P: %e, Sum Q: %e" % (sc, st)
        print "*** ERROR: st does not sum up to 1. Bailing out .."
        sys.exit(2)

    div = 0.
    for t, v in _s.iteritems():
        pts = v / ssum

        ptt = epsilon
        if t in _t:
            ptt = gamma * (_t[t] / tsum)

        ckl = (pts - ptt) * math.log(pts / ptt)

        div +=  ckl

    return div
#end of kldiv


if __name__== "__main__":

    d1 = """Many research publications want you to use BibTeX, which better
    organizes the whole process. Suppose for concreteness your source
    file is x.tex. Basically, you create a file x.bib containing the
    bibliography, and run bibtex on that file."""
    d2 = """In this case you must supply both a \left and a \right because the
    delimiter height are made to match whatever is contained between the
    two commands. But, the \left doesn't have to be an actual 'left
    delimiter', that is you can use '\left)' if there were some reason
    to do it."""

    d1 = """haha this is really funny"""
    d2 = """what is so funny ?"""

    d3 = """haha is this really cool"""
    d3 = """ 6565yyy"""
    print tokenize(d3)
    print "KL-divergence between d1 and d2:", kldiv(tokenize(d1), tokenize(d3))
    print "KL-divergence between d2 and d1:", kldiv(tokenize(d2), tokenize(d1))

