import os
import json

MIN_FLOAT = -3.14e100


# load start_P, trans_P, emit_P
if os.path.exists('../prob.json'):
    f = open('../prob.json')
    data = json.load(f)
    start_P = data['PI']
    trans_P = data['B']
    emit_P = data['A']
else:
    from .prob_start import P as start_P
    from .prob_trans import P as trans_P
    from .prob_emit import P as emit_P

# B - begin
# M - Mid
# S - Single
# E - End
STATES = 'BMES'
# 每个状态的前一个状态可能出现的状态  比如  E -> B  S -> B  B不能转到B M不能转到B
PrevStatus = {
    'B': 'ES',
    'M': 'MB',
    'S': 'SE',
    'E': 'BM'
}


def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]  # tabular
    path = {}
    for y in states:  # init
        V[0][y] = start_p[y] + emit_p[y].get(obs[0], MIN_FLOAT)
        path[y] = [y]
    for t in range(1, len(obs)):
        V.append({})
        newpath = {}
        for y in states:
            em_p = emit_p[y].get(obs[t], MIN_FLOAT)
            (prob, state) = max(
                [(V[t - 1][y0] + trans_p[y0].get(y, MIN_FLOAT) + em_p, y0) for y0 in PrevStatus[y]])
            V[t][y] = prob
            newpath[y] = path[state] + [y]
        path = newpath

    (prob, state) = max((V[len(obs) - 1][y], y) for y in 'ES')

    return prob, path[state]


def cut(sentence):
    global emit_P
    prob, pos_list = viterbi(sentence, STATES, start_P, trans_P, emit_P)
    begin, nexti = 0, 0
    for i, char in enumerate(sentence):
        pos = pos_list[i]
        if pos == 'B':
            begin = i
        elif pos == 'E':
            yield sentence[begin:i + 1]
            nexti = i + 1
        elif pos == 'S':
            yield char
            nexti = i + 1
    if nexti < len(sentence):
        yield sentence[nexti:]
