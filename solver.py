import sys
from pathlib import Path
import numpy as np

wordspath = Path(sys.argv[1])
wordstxt = wordspath.read_text()
words = set([w for w in wordstxt.split("\n") if not len(w.strip()) == 0])

print(f"Number of characters: {len(list(words)[0])}")

def chars_matching(w1, w2):
    matching = 0
    match_frame = ""
    for i in range(len(w1)):
        if w1[i] == w2[i]:
            matching += 1
            match_frame += w1[i]
        else:
            match_frame += " "
    return matching, match_frame

def find_recommendations(words):
    # Go through each word, and find the conditional expected number of words remaining if this word is chosen
    # The best word is the word with the lowest expected number of words remaining after it is chosen.
    #
    # The expexted words remaining is calculated by determining how many "groups" of words remain after select this one. For example,
    # the ideal word distribution is if there are 4 words of length 4 and selecting the word gives the index of the word that it belongs to
    #
    # WADE
    # WIMP
    # TALL
    # MODI
    # BILE
    #
    # Selecting WADE has the following probabilities:
    # 1/5) WADE is the answer
    # 1/5) WIMP is the answer, and M = 1 (W)
    # 1/5) TALL is the answer, and M = 1 (A)
    # 1/5) MODI is the answer, and M = 1 (D)
    # 1/5) BILE is the answer, and M = 1 (E)
    # In this case, selecting WADE only excludes WADE, because either WADE is the answer of 4/5 any of the other words is the answer.
    #
    # Instead, if we select TALL, then
    # 1/5) WADE is the answer, and M = 1
    # 1/5) WIMP is the answer, and M = 0
    # 1/5) TALL is the answer
    # 1/5) MODI is the answer, and M = 0
    # 1/5) BILE is the answer, and M = 1
    # Now we have two groups, M=0 and M=1, with a 50% chance of each, meaning the expected number of words remaining is 0.5*2+0.5*2 = 2 instead of
    # 4 when WADE is selected.
    # 
    # Let M(W1, W2) be a function given two words maps to the number of characters matching.
    # Best word = argmax_w(E(M(w, w2) | A=w2))

    words = sorted(words)
    expected = [0 for _ in words] # expected words remaining for each word (index)
    for i, w in enumerate(words):
        groups = {m: 0 for m in range(len(w)+1)}
        for j, w2 in enumerate(words):
            if i != j:
                m, _ = chars_matching(w, w2)
                groups[m] += 1
        counts = [c for c in groups.values() if c > 0]
        counts = np.repeat(counts, counts)
        expected[i] = np.average(counts)
        # print(f"{w}: {sorted(counts)} ({expected[i]})")

    return sorted([(expected[i], w) for i, w in enumerate(words)])


while True:
    if len(words) == 1:
        print("Answer is:", words.pop())
        break
    elif len(words) == 0:
        print("ERROR: No more words match criteria")
        break

    recommendations = find_recommendations(words)
    best = recommendations[0]
    print(f"Options remaining (recommendation: {best[1]}, expected words remaining {best[0]:.02f}):")
    for word in sorted(words):
        print(f"- {word}")

    print("Enter word chosen and number of characters matched (e.g. WORD, 3)")
    choice = input("> ")
    chosen, matched = choice.split(",")
    if chosen not in words:
        print("Word is not in list")
        continue
    print(f"Word {chosen} chosen, excluding all words that do not have same number of words")
    words.remove(chosen)

    matching = []
    for w in sorted(words):
        actual, match_frame = chars_matching(w, chosen)
        if actual == int(matched):
            # Word is a candidate
            print(f"OK {w} ({match_frame})")
            matching.append(w)
        else:
            print(f"NO {w} ({match_frame}): {actual} instead of {matched}")
    words = set(matching)



