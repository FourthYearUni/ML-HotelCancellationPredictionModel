"""
@brief:
Provides modules to do exploratory data analysis on given dataframes.
@author: Alain Mugisha(U2083264)
"""

from matplotlib import pyplot as pylt
from sklearn.cluster import KMeans
import pandas as pd

from plots import Charts, Maps
from cleaner import Cleaner

from feature_engineering import FeatureEngineering


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

        self.fe = FeatureEngineering(self.data_frame)
        self.fe.create_month_year()
        self.fe.create_duration()
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

        df, bin_labels = self.fe.binning("duration")

        grouped = (
            df.groupby("bin_duration")["bin_duration"]
            .count()
            .reset_index(name="count")
        )

        return grouped, bin_labels

    def get_geographical_origins(self):
        """
        Provides a dataframe for charting country origins
        """
        grouped = (
            self.data_frame.groupby("country")["country"]
            .count()
            .reset_index(name="count")
        )

        return grouped.sort_values(by="count", ascending=False).head(10)


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
    properties = df_duration[0]["bin_duration"].values.tolist()
    values = df_duration[0]["count"].values.tolist()
    y_lbl_duration = "Number of Bookings"
    x_lbl_duration = "Range of duration"
    title = "Range of duration of stays"
    eda.charts.bar_chart(
        values=values,
        properties=df_duration[1],
        y_axis_lbl=y_lbl_duration,
        title=title,
        x_axis_lbl=x_lbl_duration
    )

    # Top 10 countries with the most customers
    df_geo_origins = eda.get_geographical_origins()
    properties_ctr = df_geo_origins["country"].values.tolist()
    values_ctr = df_geo_origins["count"].values.tolist()
    title_ctr = "Guest country of origin"
    labels_ctr = ["country", "count"]
    eda.charts.bar_chart(
        values=values_ctr,
        properties=properties_ctr,
        y_axis_lbl=labels_ctr[1],
        title=title_ctr,
        x_axis_lbl=labels_ctr[0]
    )
    pylt.show()
