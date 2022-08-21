from util.constants import characters
import random, time

# Use Leitner algorithm
#
# https://ncase.me/remember/
NUM_LEVELS = 7
MAX_NEW_CARDS = 5

def init():
    scores = {}
    for c in characters:
        scores[c] = 0
    is_seen = {}

    return {"scores":scores, "is_seen":is_seen, "current":None}

TODO: from here - think about the loop
def get_next_character(status, input):
    print("Scores are", scores, "is_seen", is_seen)

    if len(is_seen) > MAX_NEW_CARDS:
        scores_to_choose_from = dict([(a, b) for a, b in scores.items() if a in is_seen])
    else:
        scores_to_choose_from = scores

    lowest_scores = [(a, b) for (a, b) in scores_to_choose_from.items() if b == min(scores_to_choose_from.values())]

    selection, score = random.choice(lowest_scores)
    is_seen.add(selection)

    if score == 0:
        print("Show user", selection)
    else:
        print("What is", selection)

    time.sleep(0.5)

    is_response_correct = input("is answer correct?")
    if int(is_response_correct) == 1:
        scores[selection] = scores[selection] + 1
        if scores[selection] == NUM_LEVELS - 1:
            print("Completed", selection)
            is_seen.remove(selection)

        if min(scores.values()) == NUM_LEVELS - 1:
            print("Completed it all!")
            for c in characters:
                scores[c] = 0
            is_seen.clear()
    else:
        scores[selection] = 0
