# Fallout Hacking Solver

A small Python program that will solve your Fallout programming challenges for you.

## Installing
- Python 3
- Numpy

## Usage

Enter the list of all the words in the puzzle to a line separated file, e.g. `words.txt`:
```
PINPOINTED
CONSISTING
CONSPIRING
CONDUCTING
REASONABLY
```

Then, run the solver:
```
python solver.py words.txt
```

The solver will first recommend the word to pick to solve it as fast as possible:

```
C:\dev\fallout>python solver.py words.txt
Number of characters: 10
Options remaining (recommendation: CONDUCTING, expected words remaining 1.00):
- CONDUCTING
- CONSISTING
- CONSPIRING
- PINPOINTED
- REASONABLY
```

You then go back to the game and click the CONDUCTING word and see how many characters matched:

```
CONDUCTING, 7/10 matching
```

I then enter `CONDUCTING,7` into the tool and hit enter, and it will automatically exclude all the words that don't match and
tell you what is the answer or the next recommendation to select until only 1 remains.

```
Enter word chosen and number of characters matched (e.g. WORD, 3)
> CONDUCTING,7
Word CONDUCTING chosen, excluding all words that do not have same number of words
OK CONSISTING (CON   TING)
NO CONSPIRING (CON    ING): 6 instead of 7
NO PINPOINTED (  N       ): 1 instead of 7
NO REASONABLY (          ): 0 instead of 7
Answer is: CONSISTING
```

In the example above, we find the answer is `CONSISTING` because it's the only option remaining.

### Related
- https://hackfallout.analogbit.com/