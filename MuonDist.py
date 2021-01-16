import random
import numpy as np
import matplotlib.pyplot as plt
from itertools import chain
from math import sqrt
from scipy.stats import norm


class MuonDistribution:
    """Docstring for MuonDistribution. """
    def __init__(self,
                 numEvents,
                 prob_3by4_events,
                 prob_2by4_events,
                 prob_1by4_events,
                 xmin,
                 xmax,
                 ymin,
                 ymax,
                 noise=0.05):
        """TODO: to be defined.

        :numEvents: TODO
        :prob_3by4_events: TODO
        :prob_2by4_events: TODO
        :prob_1by4_events: TODO

        """
        self._numEvents = numEvents
        self._prob_3by4_events = prob_3by4_events + random.uniform(0, noise)
        self._prob_2by4_events = prob_2by4_events + random.uniform(0, noise)
        self._prob_1by4_events = prob_1by4_events + random.uniform(0, noise)
        self._xmin, self._xmax = xmin, xmax
        self._ymin, self._ymax = ymin, ymax

    def getEventEfficiency(self):
        events_3 = round(self._prob_3by4_events * self._numEvents)
        events_2 = round(self._prob_2by4_events * self._numEvents)
        events_1 = round(self._prob_1by4_events * self._numEvents)
        events_4 = self._numEvents - events_1 - events_2 - events_3
        return events_1, events_2, events_3, events_4

    def getRandomMuonHit(self, event_type):
        if event_type == 4:
            event = (random.randint(self._xmin, self._xmax),
                     random.randint(self._ymin, self._ymax),
                     random.randint(self._xmin, self._xmax),
                     random.randint(self._ymin, self._ymax))
            return event
        elif event_type == 3:
            event = [
                -1,
                random.randint(self._ymin, self._ymax),
                random.randint(self._xmin, self._xmax),
                random.randint(self._ymin, self._ymax)
            ]
            random.shuffle(event)
            return tuple(event)
        elif event_type == 2:
            event = [
                -1, -1,
                random.randint(self._ymin, self._ymax),
                random.randint(self._xmin, self._xmax)
            ]
            random.shuffle(event)
            return tuple(event)
        else:
            event = (-1, -1, -1, -1)
            return event

    def getRandomVariable(self):
        mean = (self._xmin + self._xmax) / 2
        std = random.randrange(1, 3)
        draw = norm.ppf(np.random.random(100), loc=mean, scale=std).astype(int)
        return draw[0]

    def getGaussianMuonHit(self, event_type):
        if event_type == 4:
            event = (self.getRandomVariable(), self.getRandomVariable(),
                     self.getRandomVariable(), self.getRandomVariable())
            return event
        elif event_type == 3:
            event = [
                -1,
                self.getRandomVariable(),
                self.getRandomVariable(),
                self.getRandomVariable()
            ]
            random.shuffle(event)
            return tuple(event)
        elif event_type == 2:
            event = [
                -1, -1,
                self.getRandomVariable(),
                self.getRandomVariable()
            ]
            random.shuffle(event)
            return tuple(event)
        else:
            event = (-1, -1, -1, -1)
            return event

    def getLeadBrickMuonHit(self):
        pass

    def getShower(self, muonDist):
        e1, e2, e3, e4 = self.getEventEfficiency()
        i = 0
        hits4 = []
        hits3 = []
        hits2 = []
        hits1 = []
        while i != e4:
            hits4.append(muonDist(4))
            if i <= e1:
                hits1.append(muonDist(1))
            if i <= e2:
                hits2.append(muonDist(2))
            if i <= e3:
                hits3.append(muonDist(3))
            i += 1
        hit_sep = [hits1, hits2, hits3, hits4]
        hits = list(chain.from_iterable(hit_sep))[:self._numEvents]
        random.shuffle(hits)
        return np.array(hits, dtype=object)



if __name__ == "__main__":
    x = MuonDistribution(20, 0.25, 0.12, 0.03, 1, 11, 1, 11)
    i = x.getShower()
    x1, y1, x2, y2 = i[0]
    print(i[0])
    print(x1)
