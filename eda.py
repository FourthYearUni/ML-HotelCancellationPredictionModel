"""
@brief:
Provides modules to do exploratory data analysis on given dataframes.
@author: Alain Mugisha(U2083264)
"""

from pandas import DataFrame
from matplotlib import pyplot as pylt
from plots import Charts
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
        self.cleaner = Cleaner()
        self.data_frame = self.cleaner.data_frame

    def guests_each_month(self):
        """
        Provides of a graphical representation
        of the number of guests per Month/Year combination
        """
        grouped = (
            self.data_frame.groupby("monthYear")["monthYear"]
            .count()
            .reset_index(name="count")
        )
        return grouped


if __name__ == "__main__":
    eda = EDA()
    df_guests_each = eda.guests_each_month()
    DataFrame(df_guests_each).to_excel("output.xlsx")
    values = df_guests_each["monthYear"].values.tolist()
    properties = df_guests_each["count"].values.tolist()
    labels = ["Number of bookings", "Month/Year"]

    title = "Bookings each month"
    plt_canc = eda.charts.line_chart(properties, values, labels, title)
    pylt.show()
