"""Find solution to Party problem
Use:
--ceomustattend 
to force the CEO to attend
"""

import json
import sys

from pyevolve import G1DList
from pyevolve import GAllele
from pyevolve import GSimpleGA
from pyevolve import Initializators
from pyevolve import Mutators
from pyevolve import Scaling


ceo_must_attend = False
boss_indices = []
names = []
scores = []


def get_party_score(party_attendances):
    total_score = 0
    for person_index, is_attending in enumerate(party_attendances):
        if is_attending:
            boss_index = boss_indices[person_index]
            if boss_index is not None:
                if not party_attendances[boss_index]:
                    total_score += scores[person_index]
            else:
                total_score += scores[person_index]
    return total_score

def get_alleles():
    value_ranges = [[0, 1]] * len(names)
    if ceo_must_attend:
        ceo_index = boss_indices.index(None) 
        value_ranges[ceo_index] = [1]
    alleles = GAllele.GAlleles()
    for value_range in value_ranges:
        allele = GAllele.GAlleleRange(*value_range)
        alleles.add(allele)
    return alleles

def get_best_party():
    genome = G1DList.G1DList(len(names))
    alleles = get_alleles()
    genome.setParams(allele=alleles)
    genome.mutator.set(Mutators.G1DListMutatorAllele)
    genome.initializator.set(Initializators.G1DListInitializatorAllele)
    genome.evaluator.set(get_party_score)
    ga = GSimpleGA.GSimpleGA(genome)
    pop = ga.getPopulation()
    pop.scaleMethod.set(Scaling.SigmaTruncScaling)
    pop.setPopulationSize(500)
    ga.setGenerations(200)
    ga.evolve()
    return ga.bestIndividual()

def init(user_input):
    global boss_indices
    global names
    global scores
    people = json.loads(user_input)
    names = [person['name'] for person in people]
    for person in people:
        scores.append(person['party-animal-score'])
        boss_index = names.index(person['boss']) if person['boss'] else None
        boss_indices.append(boss_index)

def main():
    init(sys.stdin.read())
    best_party = get_best_party()
    attendances = best_party.genomeList
    for index, attendance in enumerate(attendances):
        if attendance:
            print names[index]

if __name__ == '__main__':
    ceo_must_attend = '--ceomustattend' in sys.argv
    main()