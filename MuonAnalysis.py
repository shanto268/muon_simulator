import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from Histo2d import Histo2D


def describe_helper(series):
    splits = str(series.describe()).split()
    keys, values = "", ""
    for i in range(0, len(splits), 2):
        keys += "{:2}\n".format(splits[i])
        values += "{:>2}\n".format(splits[i + 1])
    return keys, values


class MuonAnalysis:
    """Docstring for MuonAnalysi. """
    def __init__(self, hits, d, dlead):
        """TODO: to be defined.

        :hits: TODO

        """
        self._hits = hits
        self._d = d / 2  # telescope units 100 cm / 5 cm
        self._d_lead = dlead
        self.df = self.getDataFrame()

    def get(self):
        pass

    def getDataFrame(self):
        x1s = []
        x2s = []
        y1s = []
        y2s = []
        theta = []
        thetax = []
        thetay = []
        thetaz = []
        for i in self._hits:
            x1, y1, x2, y2 = i
            x1s.append(x1)
            x2s.append(x2)
            y1s.append(y1)
            y2s.append(y2)
            if -1 not in i:
                theta.append((y2 - y1 / x2 - x1) * (180 / np.pi))
                thetax.append(np.arctan(y1 / x1) * (180 / np.pi))
                thetay.append(np.arctan(x1 / y1) * (180 / np.pi))
                thetaz.append(
                    np.arctan(np.sqrt(x1**2 + y1**2) / self._d) *
                    (180 / np.pi))
            else:
                theta.append(np.nan)
                thetax.append(np.nan)
                thetay.append(np.nan)
                thetaz.append(np.nan)
        columns = [
            'x1', 'y1', 'x2', 'y2', 'thetaxy', 'thetax', 'thetay', 'thetaz'
        ]
        df = pd.DataFrame(list(
            zip(x1s, y1s, x2s, y2s, theta, thetax, thetay, thetaz)),
                          columns=columns)
        return df

    def getZAnglePlot(self, bins=90, ranges=(-90, 90)):
        plt.hist(self.df.thetaz.values,
                 bins=bins,
                 range=ranges,
                 histtype='step')
        plt.figtext(.15, .65,
                    describe_helper(pd.Series(self.df.thetaz.values))[0],
                    {'multialignment': 'left'})
        plt.figtext(0.20, .65,
                    describe_helper(pd.Series(self.df.thetaz.values))[1],
                    {'multialignment': 'right'})
        plt.show()

    def keepEvents(self, term, value, cond):
        if cond == "<":
            self.self.df = self.self.df[self.self.df[term] < value]
        elif cond == ">":
            self.self.df = self.self.df[self.self.df[term] > value]
        elif cond == "==":
            self.self.df = self.self.df[self.self.df[term] == value]
        elif cond == ">=":
            self.self.df = self.self.df[self.self.df[term] >= value]
        elif cond == "<=":
            self.self.df = self.self.df[self.self.df[term] <= value]
        elif cond == "!=":
            self.self.df = self.self.df[self.self.df[term] != value]

    def x(self, t):
        asymT1 = self.df["x1"].values
        asymT3 = self.df["x2"].values
        return asymT1 + asymT3 * t

    def y(self, t):
        asymT2 = self.df["y1"].values
        asymT4 = self.df["y2"].values
        return asymT2 + asymT4 * t

    def z(self, t):
        return -(self._d) + self._d * t

    def getTValue(self):
        return -(self._d) - self._d_lead

    def get2DTomogram(self, pdfv=False, nbins=22, title="", reload=True):
        # self.keep4by4Events()
        xmin = -350
        xmax = 100
        ymin = -350
        ymax = 100
        t = self.getTValue()
        xx = self.x(t)
        yy = self.y(t)
        self.get2DHistogram(xx,
                            yy,
                            "{} Z Plane of Lead Brick".format(title),
                            "Asymmetry in X",
                            "Asymmetry in Y",
                            xmin,
                            xmax,
                            ymin,
                            ymax,
                            nbins,
                            pdf=pdfv,
                            zLog=False)

    def get2DHistogram(self,
                       xvals,
                       yvals,
                       title,
                       xlabel,
                       ylabel,
                       xmin,
                       xmax,
                       ymin,
                       ymax,
                       nbins=150,
                       pdf=False,
                       zLog=True):
        # name = title.replace(" ", "") + "_run_" + self.runNum
        name = " "
        if not pdf:
            Histo2D(name,
                    title,
                    xlabel,
                    nbins,
                    xmin,
                    xmax,
                    xvals,
                    ylabel,
                    nbins,
                    ymin,
                    ymax,
                    yvals,
                    pdf,
                    zIsLog=zLog)
        else:
            return Histo2D(name,
                           title,
                           xlabel,
                           nbins,
                           xmin,
                           xmax,
                           xvals,
                           ylabel,
                           nbins,
                           ymin,
                           ymax,
                           yvals,
                           pdf,
                           zIsLog=zLog)
