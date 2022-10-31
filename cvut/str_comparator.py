__all__ = ["compute_strsim", "is_total_matched", "is_one_error_matched", ]


def _levenshtein(u, v):
    prev = None
    curr = list(range(0, 1+len(v)))

    # Operations: (SUB, DEL, INS)
    prev_ops = None
    curr_ops = [(0, 0, i) for i in range(len(v) + 1)]

    for x in range(1, len(u) + 1):
        prev, curr = curr, [x] + ([None] * len(v))
        prev_ops, curr_ops = curr_ops, [(0, x, 0)] + ([None] * len(v))

        for y in range(1, len(v) + 1):
            delcost = prev[y] + 1
            addcost = curr[y - 1] + 1
            subcost = prev[y - 1] + int(u[x - 1] != v[y - 1])
            curr[y] = min(subcost, delcost, addcost)

            if curr[y] == subcost:
                (n_s, n_d, n_i) = prev_ops[y - 1]
                curr_ops[y] = (n_s + int(u[x - 1] != v[y - 1]), n_d, n_i)
            elif curr[y] == delcost:
                (n_s, n_d, n_i) = prev_ops[y]
                curr_ops[y] = (n_s, n_d + 1, n_i)
            else:
                (n_s, n_d, n_i) = curr_ops[y - 1]
                curr_ops[y] = (n_s, n_d, n_i + 1)

    return curr[len(v)], curr_ops[len(v)]


def compute_strsim(str1, str2, symmetric=True):
    if str1 == '' or str2 == '':
        return 0

    # str1 (gt) <- str2 (pred)
    _, (cer_s, cer_i, cer_d) = _levenshtein(str1, str2)
    cer = (cer_s + cer_i + cer_d) / len(str1)
    sim1 = 1.0 - cer

    if not symmetric:
        return sim1

    # str2 (gt) <- str1 (pred)
    _, (cer_s, cer_i, cer_d) = _levenshtein(str1, str2)
    cer = (cer_s + cer_i + cer_d) / len(str1)
    sim2 = 1.0 - cer

    # Average sim
    return 0.5 * (sim1 + sim2)


def is_total_matched(gt_str, pred_str):
    sim = compute_strsim(gt_str, pred_str, symmetric=False)
    return sim == 1


def is_one_error_matched(gt_str, pred_str):
    sim = compute_strsim(gt_str, pred_str, symmetric=False)
    thr = (len(gt_str) - 1) / len(gt_str)
    return sim >= thr
