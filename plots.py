"""
@brief:
Provides methods to plot data. The methods are data agnostic for reuse.

@author: Alain Christian (U2083264)
"""

import matplotlib.pyplot as plt


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
        fig, ax = plt.subplots()
        labels = properties
        ax.bar(properties, values, label=labels)
        ax.set_ylabel(y_axis_lbl)
        ax.legend(title=title)

        return plt
