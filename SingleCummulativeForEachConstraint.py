import time
import argparse

from ConstraintRulesGenerator import ConstraintRulesGenerator
from ExperimentRunner import ExperimentRunner


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--start',
                        metavar='start',
                        type=int,
                        help='start',
                        default=0)
    parser.add_argument('--end',
                        metavar='end',
                        type=int,
                        help='end',
                        default=1011)
    parser.add_argument('--timeout',
                        metavar='timeout',
                        type=float,
                        help='timeout',
                        default=5)
    args = parser.parse_args()
    start = args.start
    end = args.end
    timeout = args.timeout
    print("timeout={}, start={}, end={}".format(timeout, start, end))

    rulesGenerator = ConstraintRulesGenerator()
    rulesDict = rulesGenerator.singleCummulativeForEachConstraint()

    runner = ExperimentRunner()

    before = time.time()
    runner.run("SingleCummulativeForEachConstraint", rulesDict, timeout, start, end)
    print("time={} seconds".format(time.time()-before))
