# DFA Minimizer

A Python program that minimizes a deterministic finite automaton (DFA): it removes unreachable states and merges equivalent states using the classic table-filling (Myhill-Nerode) algorithm, then prints the resulting minimized automaton in the same input format.

## Description

This program reads a DFA definition (states, alphabet, accepting states, start state, and transition function) from standard input, then performs two standard minimization steps:

1. **Unreachable state removal** — a depth-first search from the start state finds every state reachable via some sequence of transitions; any state not reached is discarded.
2. **Equivalent state merging** — a table-filling algorithm marks pairs of states as "distinguishable" if one is accepting and the other isn't, or if they transition on some input to a pair of states that are themselves already marked distinguishable. This repeats until no more pairs can be marked. Any remaining unmarked pair of states is equivalent and gets merged into one, with all incoming transitions redirected accordingly.

The final, minimized automaton (states, alphabet, accepting states, start state, and transitions) is printed to standard output in the same format it was read in.

## Requirements

- Python 3.7+
- [NumPy](https://numpy.org/)

```bash
pip install numpy
```

## Usage

```bash
python dfa_minimizer.py < input.txt
```

or interactively:

```bash
python dfa_minimizer.py
# then type/paste the input and send EOF (Ctrl+D on Unix, Ctrl+Z then Enter on Windows)
```

## Input Format

Input is read from stdin, one item per line:

```
state1,state2,state3,...
input_symbol1,input_symbol2,...
accepting_state1,accepting_state2,...
start_state
state,input_symbol->next_state
state,input_symbol->next_state
...
```

- **Line 1**: comma-separated list of all state names
- **Line 2**: comma-separated list of alphabet symbols
- **Line 3**: comma-separated list of accepting state names
- **Line 4**: the start state's name
- **Remaining lines**: one transition per line, in the form `state,symbol->next_state`. A transition can also target multiple states in the form `state,symbol->next1,next2,...` (parsed as multiple individual transitions from that state on that symbol)

### Example

```
q0,q1,q2,q3
0,1
q3
q0
q0,0->q1
q0,1->q2
q1,0->q3
q1,1->q2
q2,0->q2
q2,1->q2
q3,0->q3
q3,1->q3
```

## Output Format

The minimized automaton is printed in the same structure as the input:

```
<states>
<alphabet>
<accepting states>
<start state>
<state>,<symbol>-><next state>
...
```

## Algorithm Notes

- **Reachability pruning** happens first, via DFS from the start state, so equivalence checking only considers states that can actually be reached.
- **Table filling** uses an `n x n` NumPy matrix where a `1` marks a pair of states as distinguishable; it iterates until a fixed point is reached (no new pairs get marked in a full pass).
- **State merging** processes equivalent pairs from highest index to lowest, redirecting every transition that pointed to the higher-indexed state so it points to its equivalent lower-indexed partner, then removing the now-redundant state (updating the start state's identity if it happens to be the one removed).
- This implementation assumes the input DFA is already fully specified (every state has a transition for every alphabet symbol); it doesn't add or handle an implicit "dead" trap state for missing transitions.

## License

Feel free to use, modify, and distribute this project. Consider adding an explicit license file (e.g. MIT) if you plan to share it publicly.
