#Genetic Algorithm - Finite State Machine

from pprint import pprint
import secrets

from AntTrail.AntBase import Action

GENES = 16
TRANSITIONS = 8  # 3 binary-ish input states = 8 transitions
ANTS = 1024

class FSAGene:
    action = Action.ADVANCE
    transitions = [0 for i in range(TRANSITIONS)]

    def __repr__(self):
        return "<FSAGene: action: {}, transitions: {}>".format(self.action, self.transitions)


class FSMAnt:
    def __init__(self, id, epoch= 1, randomise = False, genome = None):
        self.id = id
        self.epoch = epoch


        if not genome:
            self.genes = [FSAGene() for _ in range(GENES)]
        else:
            self.genes = genome

        self.state = 0

        if randomise:
            self.randomise_genome()


    def randomise_genome(self):
        #convert to list once for rand init
        actions = list(Action)

        for gene in self.genes:
            gene.action = secrets.choice(actions)
            gene.transitions = [secrets.randbelow(GENES) for _ in range(TRANSITIONS)]


    def next(self, view):
        #print("Ant {} called for next".format(self.id))

        #convert view data into FSM input
        input_view = 0
        input_view = input_view + (4 if view['left'] else 0)
        input_view = input_view + (2 if view['middle'] else 0)
        input_view = input_view + (1 if view['right'] else 0)

        #print(view, input_view)

        # lookup next state
        current_state = self.genes[self.state]
        next_state = current_state.transitions[input_view]

        #print(current_state)

        #change state and return action
        self.state = next_state
        #print("Ant {} action {}".format(self.id, self.genes[self.state].action))
        return self.genes[self.state].action


    def reset(self):
        self.state = 0


    def __repr__(self):
        repr = "<FSMAnt: ID: {}\n".format(self.id, self.genes)
        for gene in self.genes:
            repr = repr + "  {}\n".format(gene)
        repr = repr + ">"

        return repr


class AntNest:
    def __init__(self):
        self.ants = []
        self.successfull_ants = []

        self._initialise_ants()


    def epoch(self, epoch, results):
        print("Epoch {}".format(epoch))

        #GA cross breed ANTS
        self.cross_breed(epoch, results)

        #random mutation
        self.mutate()



    def mutate(self):
        actions = list(Action)
        #randomly mutate 10%
        mutations = secrets.randbelow( int(len(self.ants)*0.16) )

        for case in range(mutations):
            ant = secrets.choice(self.ants)

            #determine what gene to mutate
            gene_no = secrets.randbelow(GENES)
            gene = ant.genes[gene_no]

            #determine which part of gene
            target = secrets.randbelow(TRANSITIONS+1)
            if target == 8:
                gene.action = secrets.choice(actions)
            else:
                gene.transitions[target] = secrets.randbelow(GENES)



    def cross_breed(self, epoch, results):

        #best ant progress
        best_progress = max([ant["trail progress"] for ant in results])
        print("Best ant progessed {} pheremone steps".format(best_progress))

        worst_progress = min([ant["trail progress"] for ant in results])
        print("Worst ant progessed {} pheremone steps".format(worst_progress))

        #sort the ants based on progress
        sorted_results = sorted(results, key=lambda x: x["trail progress"], reverse=True)

        #keep the best half and discard the rest
        new_ant_parents = [res["id"] for res in sorted_results]
        cut = ANTS//2
        new_ant_parents = new_ant_parents[0:cut]

        #randomly make pairs - then produce 4 new children => new ants
        pairings = []
        while len(new_ant_parents)>0:
            a = secrets.choice(new_ant_parents)
            new_ant_parents.remove(a)
            b = secrets.choice(new_ant_parents)
            new_ant_parents.remove(b)

            pairings.append([a,b])

        #print("created {} new pairings".format(len(pairings)))

        new_ants = []
        for pair in pairings:
            children = self.create_children(pair[0], pair[1], 4)
            new_ants = new_ants + children

        #print("created {} new ants".format(len(new_ants)))

        #clead up the ids and epochs
        new_epoch = epoch + 1
        for index,ant in enumerate(new_ants):
            ant.id = index
            ant.epoch = new_epoch

        #update to new ant list
        self.ants = new_ants


    def create_children(self, a, b, count):
        children = []
        for i in range(count):
            #randomly select cross over point
            xpoint = secrets.randbelow(GENES)
            gene_sequence = self.ants[a].genes[0:xpoint] + self.ants[b].genes[xpoint:]

            child = FSMAnt(0, randomise=False, genome=gene_sequence)

            children.append(child)

        return children


    def get_ant_list(self):
        return self.ants


    def _initialise_ants(self):
        self.ants = [FSMAnt(i, randomise=True) for i in range(ANTS)]
