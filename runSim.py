# -*- coding: utf-8 -*-
"""
=======================================
Program : muon_simulator/runSim.py
=======================================
"""
__author__ = "Sadman Ahmed Shanto"
__date__ = "01/15/2021"
__email__ = "sadman-ahmed.shanto@ttu.edu"

import numpy as np
import matplotlib.pyplot as plt
from MuonDist import MuonDistribution
from MuonAnalysis import MuonAnalysis

# main function
if __name__ == "__main__":
    sep_distance = 40  # # telescope units (2 m / 5 cm)
    dlead = (0.42 * 100) / 5
    events = 20000
    p3by4 = 0.25
    p2by4 = 0.12
    p1by4 = 0.03
    xmin = 1
    xmax = 11
    ymin = 1
    ymax = 11

    md = MuonDistribution(events, p3by4, p2by4, p1by4, xmin, xmax, ymin, ymax)
    hits = md.getShower(md.getGaussianMuonHit)
    print("Muon Shower Done")
    ma = MuonAnalysis(hits, sep_distance, dlead)
    ma.get2DTomogram()
