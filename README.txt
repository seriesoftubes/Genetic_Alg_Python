Uses GA to find the optimal combination of people to invite to a party.
The objective function is nonlinear; it sums the scores of the people at the party, but if a person's boss is at the party, their score becomes zero.

Usage:
>>> python partysolver.py < people.json


Requires:
PyEvolve