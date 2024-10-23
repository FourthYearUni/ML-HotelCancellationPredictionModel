"""
@brief:
Provides methods to plot data. The methods are data agnostic for reuse.

@author: Alain Christian (U2083264)
"""

import matplotlib.pyplot as pylt
import geopandas as gpd
from matplotlib.pyplot import xticks

from pandas import DataFrame
import numpy as np
import random


class Charts:
    """
    This class houses methods for creating charts.
    """

    def __init__(self):
        self.pylt = pylt
    @staticmethod
    def bar_chart(
        values: list,
        properties: list,
        y_axis_lbl: str,
        title: str,
        x_axis_lbl: str = None,
    ):
        """
        Creates a bar chart using a list of provided values and properties.
        """
        fig, ax = pylt.subplots(figsize=(10, 8))
        labels = properties
        colors = [
            (random.random(), random.random(), random.random(), 1) for value in values
        ]
        ax.bar(properties, values, label=labels, color=colors,)
        ax.set_ylabel(y_axis_lbl)
        ax.set_xlabel(x_axis_lbl)
        ax.set_xticklabels(properties, rotation=45)
        ax.legend(title=title)

        return pylt

    def line_chart(self, properties: list, values: list, labels: list[str], title: str):
        """
        Creates a line chart using a list of provided values and properties.
        """
        # Create a line chart
        self.pylt.figure(figsize=(8, 6))
        self.pylt.plot(properties, values, marker="o", linestyle="-")
        self.pylt.title(title)
        self.pylt.xlabel(labels[0])
        self.pylt.ylabel(labels[1])
        self.pylt.grid(True)
        self.pylt.xticks(rotation=90)
        return self.pylt

    def pie_chart(self, properties: list, values: list, title: str):
        """
        Creates a pie chart using a list of provided values
        """
        colors = [
            (random.random(), random.random(), random.random(), 1) for value in values
        ]

        # Create a pie chart
        fig, ax = pylt.subplots(figsize=(15, 15))
        ax.pie(
            values,
            labels=properties,
            colors=colors,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.85,
            labeldistance=1.5,
        )
        self.pylt.legend(properties, loc="center left", bbox_to_anchor=(1, 0.5), ncol=3)
        self.pylt.title(title)


class Maps:
    """
    This class presents methods that create various types of maps
    """

    def __init__(self):
        self.pylt = pylt

    def heat_map(self, contingency_tbl, annot=True, cmap="YlGnBu"):
        """
        Creates a heat map with the provided contigency
        """
        self.pylt.imshow(contingency_tbl, cmap, aspect="auto")
        self.pylt.colorbar()
        self.pylt.xticks(np.arange(contingency_tbl.shape[1]), contingency_tbl.columns)
        self.pylt.yticks(np.arange(contingency_tbl.shape[0]), contingency_tbl.index)
        return self.pylt
    @staticmethod
    def choropleth_map(df: DataFrame):
        """
        Returns a choropleth map
        """

        url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
        world = gpd.read_file(url)
        # Merge dataset / frame to add geospatial data

        merged_frame = world.merge(df, how="left", left_on="ISO_A3", right_on="country")
        merged_frame["country"].dropna(inplace=False)
        fig, ax = pylt.subplots(1, 1, figsize=(14, 10))

        merged_frame.plot(
            column="count",
            ax=ax,
            legend=True,
            cmap="YlGnBu",
            missing_kwds={
                "color": "lightgrey",
                "edgecolor": "red",
                "hatch": "/\/",
                "label": "Unknown values",
            },
        )

        ax.set_title("Bookings per country")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        pylt.legend(loc="lower right")

        ax.set_axis_off()
