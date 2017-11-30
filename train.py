import neat
from controller import Controller
from tetris import Tetris
from automatedTetris import AutomatedTetris, AutomatedTetrisWindow
import pickle
import numpy as np
import random

class NeuralNetworkController(Controller):
    
    def __init__(self, net):
        self.net = net

    def getMove(self, board):
        outputs = self.net.activate(board)
        move = Tetris.DOWN
        #print(outputs)
        for m in Tetris.POSSIBLE_MOVES:
            if outputs[m] > outputs[move]:
                move = m
        return move

TRIALS_PER_GENOME = 1

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        controller = NeuralNetworkController(net)
        scores = np.empty((TRIALS_PER_GENOME,1))
        for i in range(TRIALS_PER_GENOME):
            random.seed(i)
            initrandomstate = random.getstate()
            autoTetris = AutomatedTetris(controller, initrandomstate=initrandomstate,
                    recordMoves=False)
            # have the net play for at most 10 minutes
            autoTetris.play(maxMoves=AutomatedTetris.FPS*600)
            #print(autoTetris.moves)
            scores[i] = autoTetris.score()
            #+ autoTetris.gameLength/100.
        
        genome.fitness = np.mean(scores)


def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(100))

    winner = p.run(eval_genomes, 1000)

    # Display the winning genome.
    #print('\nBest genome:\n{!s}'.format(winner))

    # Show output of the most fit genome against training data.
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    with open("winner.net","wb") as f:
        pickle.dump(winner_net, f)

def playNet(filename):
    with open(filename, "rb") as f:
        winner_net = pickle.load(f)
        controller = NeuralNetworkController(winner_net) 
        random.seed(0)
        initrandomstate = random.getstate()
        autoTetris = AutomatedTetris(controller, initrandomstate=initrandomstate)
        AutomatedTetrisWindow(autoTetris).play()


#run("train_config")
playNet("winner.net")
