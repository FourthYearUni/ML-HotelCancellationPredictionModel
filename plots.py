"""
@brief:
Provides methods to plot data. The methods are data agnostic for reuse.

@author: Alain Christian (U2083264)
"""

import matplotlib.pyplot as pylt
import seaborn as sns
import numpy as np
import random


class Charts:
    """
    This class houses methods for creating charts.
    """

    def __init__(self):
        pass

    def bar_chart(self, values: list, properties: list, y_axis_lbl: str, title: str):
        """
        Creates a bar chart using a list of provided values and properties.
        """
        fig, ax = pylt.subplots()
        labels = properties
        colors = [
            (random.random(), random.random(), random.random(), 1) for value in values
        ]
        ax.bar(properties, values, label=labels, color=colors)
        ax.set_ylabel(y_axis_lbl)
        ax.legend(title=title)

        return pylt


class Maps:
    """
    This class presents methods that create various types of maps
    """

    def __init__(self):
        pass

    def heat_map(self, contingency_tbl, annot=True, cmap="YlGnBu"):
        """
        Creates a heat map with the provided heatmap
        """
        pylt.imshow(contingency_tbl, cmap, aspect="auto")
        pylt.colorbar()
        pylt.xticks(np.arange(contingency_tbl.shape[1]), contingency_tbl.columns)
        pylt.yticks(np.arange(contingency_tbl.shape[0]), contingency_tbl.index)
        return pylt
