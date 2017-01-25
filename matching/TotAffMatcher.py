import logging
import time
import uuid
from gurobipy import *

import numpy as np


class TotAffMatcher(object):
    """An iterative paper matching problem instance that tries to maximize
    the sum total affinity of all reviewer paper matches
    Attributes:
      n_Rev - the number of reviewers
      n_Pap - the number of papers
      alphas - a list of tuples of (min, max) papers for each reviewer.
      betas - a list of tuples of (min, max) reviewers for each paper.
      weights - the compatibility between each reviewer and each paper.
                This should be a numpy matrix of dimension  n_rev x n_pap.
    """

    def __init__(self, alphas, betas, weights):
        self.n_rev = np.size(weights, axis=0)
        self.n_pap = np.size(weights, axis=1)
        self.alphas = alphas
        self.betas = betas
        self.weights = weights
        self.id = uuid.uuid4()
        self.m = Model(str(self.id) + ": iterative b-matching")
        self.prev_sols = []
        self.prev_rev_affs = []
        self.prev_pap_affs = []
        self.m.setParam('OutputFlag', 0)

        # primal variables
        self.lp_vars = []
        for i in range(self.n_rev):
            self.lp_vars.append([])
            for j in range(self.n_pap):
                self.lp_vars[i].append(self.m.addVar(vtype=GRB.BINARY, name=self.var_name(i, j)))

        self.m.update()

        # set the objective (this could be sped up if need be by incorporating it into the previous loop)
        obj = LinExpr()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                obj += self.weights[i][j] * self.lp_vars[i][j]
        self.m.setObjective(obj, GRB.MAXIMIZE)

        # reviewer constraints
        for r in range(self.n_rev):
            self.m.addConstr(sum(self.lp_vars[r]) >= self.alphas[r][0], "r_l" + str(r))
            self.m.addConstr(sum(self.lp_vars[r]) <= self.alphas[r][1], "r_u" + str(r))

        # paper constraints
        for p in range(self.n_pap):
            self.m.addConstr(sum([self.lp_vars[i][p]
                                  for i in range(self.n_rev)]) >= self.betas[p][0],
                             "p_l" + str(p))
            self.m.addConstr(sum([self.lp_vars[i][p]
                                  for i in range(self.n_rev)]) <= self.betas[p][1],
                             "p_u" + str(p))

    def var_name(self, i, j):
        return "x_" + str(i) + "," + str(j)

    def sol_dict(self):
        _sol = {}
        for v in self.m.getVars():
            _sol[v.varName] = v.x
        return _sol

    def add_hard_const(self, i, j, log_file=None):
        """Add a single hard constraint to the model.
        CAUTION: if you have a list of constraints to add, use add_hard_constrs
        instead.  That function adds the constraints as a batch and will be
        faster.
        """
        solution = self.sol_dict()
        prevVal = solution[self.var_name(i, j)]
        if log_file:
            logging.info("\t(REVIEWER, PAPER) " + str((i, j)) + " CHANGED FROM: " + str(prevVal) + " -> " + str(
                abs(prevVal - 1)))
        self.m.addConstr(self.lp_vars[i][j] == abs(prevVal - 1), "h" + str(i) + ", " + str(j))

    def add_hard_consts(self, constrs, log_file=None):
        """Add a list of hard constraints to the model.
        Add a list of hard constraints in batch to the model.
        Args:
        constrs - a list of triples of (rev_idx, pap_idx, value).
        Returns:
        None.
        """
        for (rev, pap, val) in constrs:
            self.m.addConstr(self.lp_vars[rev][pap] == val,
                             "h" + str(i) + ", " + str(j))
        self.m.update()

    def num_diffs(self, sol1, sol2):
        count = 0
        for (variable, val) in sol1.items():
            if sol2[variable] != val:
                count += 1
        return count

    def solve(self, log_file=None):
        begin_opt = time.time()
        self.m.optimize()
        if self.m.status != GRB.OPTIMAL:
            raise Exception('This instance of matching could not be solved '
                            'optimally.  Please ensure that the input '
                            'constraints produce a feasible matching '
                            'instance.')

        end_opt = time.time()
        if log_file:
            logging.info("[SOLVER TIME]: %s" % (str(end_opt - begin_opt)))

        sol = {}
        for v in self.m.getVars():
            sol[v.varName] = v.x
        self.prev_sols.append(sol)
        self.save_reviewer_affinity()
        self.save_paper_affinity()

    def status(self):
        return m.status

    def turn_on_verbosity(self):
        self.m.setParam('OutputFlag', 1)

    def save_reviewer_affinity(self):
        per_rev_aff = np.zeros((self.n_rev, 1))
        sol = self.sol_dict()
        for i in range(self.n_rev):
            for j in range(self.n_pap):
                per_rev_aff[i] += sol[self.var_name(i, j)] * self.weights[i][j]
        self.prev_rev_affs.append(per_rev_aff)

    def save_paper_affinity(self):
        per_pap_aff = np.zeros((self.n_pap, 1))
        sol = self.sol_dict()
        for i in range(self.n_pap):
            for j in range(self.n_rev):
                per_pap_aff[i] += sol[self.var_name(j, i)] * self.weights[j][i]
        self.prev_pap_affs.append(per_pap_aff)

    def objective_val(self):
        return self.m.ObjVal
