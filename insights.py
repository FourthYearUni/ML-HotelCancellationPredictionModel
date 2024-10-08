"""
@brief:
This module uses the pre-processed dataframe from the cleaner
to derive insights from the data.

@author: Alain Mugisha (u2083264)
"""

from cleaner import Cleaner
from typing import List
from plots import Charts


class Insights:
    """
    Produces insights based on the passed information.
    """

    def __init__(self):
        self.cleaner = Cleaner()
        self.data_frame = self.cleaner.validate_data()

    def cancellation_percentage_per_hotel(self) -> List:
        """
        Calculates the percentage of cancellation per city
        """
        bookings_grouped = self.data_frame.groupby("hotel")["hotel"].count()
        bookings_city_canceled = (
            self.data_frame[
                (self.data_frame["is_canceled"] == True)
                & (self.data_frame["hotel"] == "City Hotel")
            ].size
            / 32
        )
        bookings_resort_canceled = (
            self.data_frame[
                (self.data_frame["is_canceled"] == True)
                & (self.data_frame["hotel"] == "Resort Hotel")
            ].size
            / 32
        )
        resort_perc = (
            bookings_resort_canceled / bookings_grouped["Resort Hotel"]
        ) * 100
        city_perc = (bookings_city_canceled / bookings_grouped["City Hotel"]) * 100

        return [resort_perc, city_perc]


if __name__ == "main":
    insight = Insights()
    plots = Charts()

    values = insight.cancellation_percentage_per_hotel()
    properties = ["% City Hotel", "% Resort Hotel"]
    y_axis_label = "Percentage of cancellation"
    title = "Percentage of cancellation per type of hotel"

    plt = plots.bar_chart(values, properties, y_axis_label, title)

    plt.show()