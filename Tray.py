import matplotlib.pyplot as plt
import numpy as np


class Tray:
    """Docstring for Tray. """
    def __init__(self, nbarx, nbary, bar_size, z_pos):
        """TODO: to be defined.

        :nbarx: TODO
        :nbary: TODO
        :bar_size: TODO
        :z_pos: TODO
        :tray_id: TODO

        """
        self._nbarx = nbarx
        self._nbary = nbary
        self._bar_size = bar_size
        self._z_pos = z_pos
        self.default_data = self.createPlane()

    def createTray(self, n):
        return [0 for i in range(n)]

    def createPlane(self):
        x = self.createTray(self._nbarx)
        y = self.createTray(self._nbary)
        return np.array([x, y])

    def getHit(self, hitTuple):
        data = np.array(self.default_data)
        for i in range(len(hitTuple)):
            if hitTuple[i] != -1:
                data[i, hitTuple[i] - 1] = 1
        return data


if __name__ == "__main__":
    x = Tray(11, 11, 0.5, 1)
    hit = x.getHit((2, 3))
    hit = x.getHit((-1, 11))  #-1 means missing
    hit = x.getHit((-1, -1))  #-1 means missing
