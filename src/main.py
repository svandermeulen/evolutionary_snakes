"""
Created on: 13-7-2018
@author: Stef
"""
import operator
import os
import shutil

from datetime import datetime
from neat.checkpoint import Checkpointer

from src.evolution.neat_snake import run_evolution, run_genome
from src.game.game_builder import GameHumanPlayer
from src.config import PATH_INPUT, HUMAN_PLAYER, PATH_OUTPUT_TEMP, PATH_OUTPUT


def run_checkpoint(path_checkpoint: str, path_neat_config: str):
    population = Checkpointer.restore_checkpoint(path_checkpoint).population
    d = {k: v.fitness for k, v in population.items() if v.fitness is not None}
    best_genome_key = max(d.items(), key=operator.itemgetter(1))[0]
    best_genome = population[best_genome_key]
    run_genome(winner=best_genome, path_neat_config=path_neat_config)

    return True


def main():
    datetime_run = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
    path_output = os.path.join(PATH_OUTPUT, datetime_run)
    os.mkdir(path_output)

    if not os.path.isdir(PATH_OUTPUT_TEMP):
        os.mkdir(PATH_OUTPUT_TEMP)
    [os.remove(os.path.join(PATH_OUTPUT_TEMP, p)) for p in os.listdir(PATH_OUTPUT_TEMP) if
     os.path.isfile(os.path.join(PATH_OUTPUT_TEMP, p))]

    path_neat_config = os.path.join(PATH_INPUT, "neat_config")

    if not HUMAN_PLAYER:
        best_genome = run_evolution(path_neat_config=path_neat_config,
                                    path_checkpoint=os.path.join(path_output, "neat-checkpoint-"))
        print('\nBest genome:\n{!s}'.format(best_genome))
        run_genome(winner=best_genome, path_neat_config=path_neat_config)
    else:
        GameHumanPlayer().execute()

    # move all created output visualizations and checkpoints
    [shutil.move(p, os.path.join(path_output, p)) for p in os.listdir(".") if
     os.path.isfile(p) and not p.endswith(".py")]

    return True


if __name__ == "__main__":

    # path_run = os.path.abspath("D:/Stack/stef/software/python/snake/output/20220104_143650")
    # path_checkpoint = os.path.join(path_run, "neat-checkpoint-20")
    # path_config = os.path.join(path_run, "neat_config")
    # run_checkpoint(path_checkpoint, path_config)

    main()
