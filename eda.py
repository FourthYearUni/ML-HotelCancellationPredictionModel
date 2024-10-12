"""
@brief:
Provides modules to do exploratory data analysis on given dataframes.
@author: Alain Mugisha(U2083264)
"""

from pandas import DataFrame, Series
from matplotlib import pyplot as pylt
from typing import List
from plots import Charts, Maps
from cleaner import Cleaner


class EDA:
    """
    Provides methods for carrying out Exploratory analysis
    on a variables
    """

    def __init__(self):
        """
        Constructor method
        """
        self.charts = Charts()
        self.maps = Maps()
        self.cleaner = Cleaner()
        self.data_frame = self.cleaner.data_frame

    def guests_each_month(self):
        """
        Provides of a graphical representation
        of the number of guests per Month/Year combination
        """
        grouped = (
            self.data_frame.groupby("YearMonth")["YearMonth"]
            .count()
            .reset_index(name="count")
        )
        return grouped

    def duration_of_stays(self):
        """
        Provides a dataframe representing the grouped duration of stays.
        """
        grouped = (
            self.data_frame.groupby("duration")["duration"]
            .count()
            .reset_index(name="count")
        )

        return grouped

    def get_geographical_origins(self):
        """
        Provides a dataframe for charting country origins
        """
        grouped = (
            self.data_frame.groupby("country")["country"]
            .count()
            .reset_index(name="count")
        )

        return grouped


if __name__ == "__main__":
    eda = EDA()

    # Graphing the bookings per month over the years
    df_guests_each = eda.guests_each_month()
    properties = df_guests_each["YearMonth"].values.tolist()
    values = df_guests_each["count"].values.tolist()
    labels = ["Year/Month", "Number of Bookings"]
    title = "Bookings each month"
    eda.charts.line_chart(properties, values, labels, title)

    # Graphing the duration of guest stays in a barchart.
    df_duration = eda.duration_of_stays()
    properties = df_duration["duration"].values.tolist()
    values = df_duration["count"].values.tolist()
    y_lbl_duration = "Stays"
    x_lbl_duration = "Duration of stays"
    title = "Duration of guest stays"
    eda.charts.bar_chart(values, properties, y_lbl_duration, title, x_lbl_duration)

    df_geo_origins = eda.get_geographical_origins()
    properties = df_geo_origins["country"].values.tolist()
    values = df_geo_origins["count"].values.tolist()
    title = "Guest country of origin"
    labels = ["country", "count"]
    eda.maps.choropleth_map(df_geo_origins)

    pylt.show()
