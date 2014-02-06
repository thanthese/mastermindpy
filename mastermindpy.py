import itertools
import random
import time

initial_state = \
    {"colors": "bdglpr",
     "slots": 4,
     "history": [{"pips": {"black": 0, "white": 2}, "guess": "lppl"},
                 {"pips": {"black": 1, "white": 1}, "guess": "bldb"}]}


def calc_pips(code, guess):
    c = list(code)
    g = list(guess)

    black = 0
    for i, _ in enumerate(c):
        if c[i] == g[i]:
            black += 1
            c[i] = None
            g[i] = None

    white = 0
    for i, _ in enumerate(c):
        if c[i] is not None and c[i] in g:
            white += 1
            j = g.index(c[i])
            c[i] = None
            g[j] = None

    return {"black": black, "white": white}


def all_combinations(colors, slots):
    combos = itertools.product(colors, repeat=slots)
    return ["".join(c) for c in combos]


def eliminate_candidates(candidates, guess, pips):
    is_plausible = lambda candidate: calc_pips(candidate, guess) == pips
    return filter(is_plausible, candidates)


def pips_hash(pips):
    return pips["black"] * 100 + pips["white"]


def score_guess(guess, candidates):
    pips_count = {}
    for code in candidates:
        h = pips_hash(calc_pips(code, guess))
        pips_count[h] = pips_count.get(h, 0) + 1
    return max(pips_count.values())


def next_guesses(candidates, all_combos):
    gs = {g: score_guess(g, candidates) for g in all_combos}
    min_score = min(gs.values())
    return [k for (k, v) in gs.iteritems() if v == min_score]


def calc_candidates_from_history(history, candidates, logging=False, show_if_less_than=20):
    total_combinations = len(candidates)
    for turn in history:
        candidates = eliminate_candidates(candidates, turn["guess"], turn["pips"])
        if logging:
            template = "After guess `{guess}` {num:,}/{total:,} ({percent:.2f}%) combinations remain."
            print template.format(guess=turn["guess"],
                                  num=len(candidates),
                                  total=total_combinations,
                                  percent=100.0 * len(candidates) / total_combinations)
            if len(candidates) < show_if_less_than:
                print "  Remaining candidate(s): {}".format(" ".join(candidates))
    return candidates


def print_next_guesses_from_state(state):
    all_combos = all_combinations(state["colors"], state["slots"])
    candidates = calc_candidates_from_history(state["history"], all_combos, logging=True)
    guesses = next_guesses(candidates, all_combos)

    print "There are {} optimal next guesses: {}".format(len(guesses), " ".join(guesses))
    plausibles = set.intersection(set(candidates), set(guesses))
    print "The {} plausible optimal guesses include: {}".format(len(plausibles), " ".join(plausibles))


def demo_solve(colors, slots):
    t = time.time()
    code = "".join([random.choice(colors) for _ in range(slots)])
    all_combos = all_combinations(colors, slots)
    candidates = all_combos

    print "The randomly selected code is `{}`.".format(code)
    tries = 1
    while len(candidates) > 1:
        print "  {} candidates remain.".format(len(candidates))
        guess = next_guesses(candidates, all_combos)[0]
        pips = calc_pips(code, guess)
        print "{}. The guess `{}` yields {} black, {} white.".format(tries, guess, pips["black"], pips["white"])
        candidates = eliminate_candidates(candidates, guess, pips)
        tries += 1

    print "{}. {} == {}".format(tries, candidates[0], code)
    print "{:.1f} seconds".format(time.time() - t)


if __name__ == "__main__":
    print_next_guesses_from_state(initial_state)
    # demo_solve("bdglpr", 4)
