#!/usr/bin/env python
"""Provides PluginInterface
"""

__author__ = "Meena Alfons"
__copyright__ = "Copyright 2020, Knowledge Representation, SatSolver Project, Group 25"
__credits__ = ["Meena Alfons"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Meena Alfons"
__email__ = "meena.kerolos@gmail.com"
__status__ = "Development"

class PluginInterface:
    def construct(self, cnfState):
        return

    def assignmentPushed(self, cnfState, variable, value):
        return

    def assignmentPoped(self, cnfState, variable, value):
        return

    def satisfiedClausesPushed(self, cnfState, variable, satisfiedClausesPriorities):
        return

    def satisfiedClausesPoped(self, cnfState, variable, satisfiedClausesPriorities):
        return