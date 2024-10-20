"""
@brief:
Provides methods to plot data. The methods are data agnostic for reuse.

@author: Alain Christian (U2083264)
"""

import matplotlib.pyplot as pylt
import seaborn as sns
import plotly.express as px
import geopandas as gpd


from pandas import DataFrame
import numpy as np
import random


class Charts:
    """
    This class houses methods for creating charts.
    """

    def __init__(self):
        pass

    def bar_chart(
        self,
        values: list,
        properties: list,
        y_axis_lbl: str,
        title: str,
        x_axis_lbl: str = None,
    ):
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
        ax.set_xlabel(x_axis_lbl)
        ax.legend(title=title)

        return pylt

    def line_chart(self, properties: list, values: list, labels: list[str], title: str):
        """
        Creates a line chart using a list of provided values and properties.
        """
        # Create a line chart
        pylt.figure(figsize=(8, 6))
        pylt.plot(properties, values, marker="o", linestyle="-")
        pylt.title(title)
        pylt.xlabel(labels[0])
        pylt.ylabel(labels[1])
        pylt.grid(True)
        return pylt

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
        pylt.legend(properties, loc="center left", bbox_to_anchor=(1, 0.5), ncol=3)
        pylt.title(title)


class Maps:
    """
    This class presents methods that create various types of maps
    """

    def __init__(self):
        pass

    def heat_map(self, contingency_tbl, annot=True, cmap="YlGnBu"):
        """
        Creates a heat map with the provided contigency
        """
        pylt.imshow(contingency_tbl, cmap, aspect="auto")
        pylt.colorbar()
        pylt.xticks(np.arange(contingency_tbl.shape[1]), contingency_tbl.columns)
        pylt.yticks(np.arange(contingency_tbl.shape[0]), contingency_tbl.index)
        return pylt

    def choropleth_map(self, df: DataFrame):
        """
        Returs a choropleth map
        """
        url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
        world = gpd.read_file(url)
        world.to_excel("output.xlsx")
        # Merge dataset / frame to add geospatial data

        merged_frame = world.merge(df, how="left", left_on="ISO_A3", right_on="country")
        merged_frame["country"].dropna(inplace=False)
        merged_frame.to_excel("country.xlsx")
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
