"""Run simple cell optimisation"""

"""
Copyright (c) 2016, EPFL/Blue Brain Project

 This file is part of BluePyOpt <https://github.com/BlueBrain/BluePyOpt>

 This library is free software; you can redistribute it and/or modify it under
 the terms of the GNU Lesser General Public License version 3.0 as published
 by the Free Software Foundation.

 This library is distributed in the hope that it will be useful, but WITHOUT
 ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
 details.

 You should have received a copy of the GNU Lesser General Public License
 along with this library; if not, write to the Free Software Foundation, Inc.,
 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

"""
This optimisation is based on L5PC optimisations developed by Etay Hay in the
context of the BlueBrain project
"""

# pylint: disable=R0914, W0403
import os
import sys

import argparse
# pylint: disable=R0914
import logging
logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import bluepyopt

# TODO store definition dicts in json
# TODO add functionality to read settings of every object from config format


import l5pc_evaluator
evaluator = l5pc_evaluator.create()


def evaluate(parameter_array):
    """Global evaluate function"""

    return evaluator.evaluate(parameter_array)

if os.getenv('L5PCBENCHMARK_USEIPYP') == '1':
    from ipyparallel import Client
    rc = Client(profile=os.getenv('IPYTHON_PROFILE'))
    lview = rc.load_balanced_view()

    map_function = lview.map_sync
else:
    map_function = None

opt = bluepyopt.optimisations.DEAPOptimisation(
    evaluator=evaluator,
    map_function=map_function,
    seed=os.getenv('BLUEPYOPT_SEED'))


def main():
    """Main"""
    parser = argparse.ArgumentParser(description='L5PC example')
    parser.add_argument('--start', action="store_true")
    parser.add_argument('--continu', action="store_false", default=False)
    parser.add_argument('--checkpoint', required=False, default=None,
                        help='Checkpoint pickle to avoid recalculation')
    parser.add_argument('--offspring_size', type=int, required=False, default=2,
                        help='number of individuals in offspring')
    parser.add_argument('--max_ngen', type=int, required=False, default=2,
                        help='maximum number of generations')
    parser.add_argument('--responses', required=False, default=None,
                        help='Response pickle file to avoid recalculation')
    parser.add_argument('--analyse', action="store_true")
    parser.add_argument('--compile', action="store_true")
    parser.add_argument('--hocanalyse', action="store_true")
    parser.add_argument(
        '--diversity',
        help='plot the diversity of parameters from checkpoint pickle file')

    args = parser.parse_args()

    if args.compile:
        logger.debug('Doing compile')
        import commands
        commands.getstatusoutput('cd mechanisms/; nrnivmodl; cd ..')

    # TODO store definition dicts in json
    # TODO add functionality to read settings of every object from config format


    if args.start or args.continu:
        logger.debug('Doing start or continue')
        opt.run(max_ngen=args.max_ngen,
                offspring_size=args.offspring_size,
                continue_cp=args.continu,
                cp_filename=args.checkpoint)


if __name__ == '__main__':
    main()
