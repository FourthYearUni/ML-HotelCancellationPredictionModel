"""
@brief:
This module uses the pre-processed dataframe from the cleaner
to derive insights from the data.

@author: Alain Mugisha (u2083264)
"""

from cleaner import Cleaner
from typing import List
from plots import Charts, Maps, pylt
from pandas import DataFrame, Series, crosstab
from typing import cast

from feature_engineering import FeatureEngineering

class Insights:
    """
    Produces insights based on the passed information.
    """

    def __init__(self):
        self.cleaner = Cleaner()
        self.data_frame = self.cleaner.validate_data()
        self.fe = FeatureEngineering(self.data_frame)
        self.fe.create_month_year()
        self.fe.create_duration()


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

    def most_ordered_meals(self) -> DataFrame:
        """
        Returns a data frame of the most ordered meal types.
        """
        meals = self.data_frame.groupby("meal")["meal"].count()
        return cast(DataFrame, meals)

    def most_booked_room_types(self) -> Series:
        """
        Returns a list of the most booked meals
        """
        # The focus is on the reserved room because at the time of
        # booking this is the room type given until it is potentially changed.
        room_type = self.data_frame.groupby("reserved_room_type")[
            "reserved_room_type"
        ].count()
        return cast(Series, room_type)

    def most_common_customer_types(self):
        """
        Returns a list of the most common customer types
        """
        # The focus is on the reserved room because at the time of
        # booking this is the room type given until it is potentially changed.
        customer_type = self.data_frame.groupby("customer_type")[
            "customer_type"
        ].count()
        return customer_type

    def get_returning_guests(self) -> float:
        """
        Returns a number of returning guests
        """
        r_guests = (
            self.data_frame[(self.data_frame["is_repeated_guest"] == True)].size / 32
        )
        return r_guests

    def correlation_between_columns(self, index, columns: list):
        """
        Returns a heat map showing the correlation between a passed list of columns
        It uses cross tabulation to show the frequency distribution of x amount of columns
        """
        contingency_tbl = crosstab(
            index=self.data_frame[index],
            columns=[self.data_frame[col] for col in columns],
            normalize="index",
        )
        return contingency_tbl


if __name__ == "__main__":
    insight = Insights()
    plots = Charts()
    maps = Maps()

    # Printing information about the percentage of cancellations per hotel.
    values = insight.cancellation_percentage_per_hotel()
    properties = ["% City Hotel", "% Resort Hotel"]
    y_axis_label = "Percentage of cancellation"
    title = "Percentage of cancellation per type of hotel"
    plt_canc = plots.pie_chart(properties, values, title)

    # Printing information about the most ordered meals.
    values = insight.most_ordered_meals().values.tolist()
    properties = ["BB", "FB", "HB", "SC", "Undefined"]
    y_axis_label = "Meal orders per meal type"
    title = "Most ordered meals per type"
    plt_meals = plots.bar_chart(values, properties, y_axis_label, title)

    # Printing information about the most sought after room types
    values = insight.most_booked_room_types().values.tolist()
    properties = ["A", "B", "C", "D", "E", "F", "G", "H", "L", "P"]
    y_axis_label = "Number of bookings"
    title = "Most sought after rooms"
    plt_rooms = plots.bar_chart(values, properties, y_axis_label, title)
    # plt_rooms.show()

    # Printing information about the most common type of customer
    values = insight.most_common_customer_types().values.tolist()
    properties = ["Contract", "Group", "Transient", "Transient-Party"]
    y_axis_label = "Number of bookings"
    title = "Most common type of customers"
    plt_customer_types = plots.bar_chart(values, properties, y_axis_label, title)
    # plt_rooms.show()

    # Printing the number of the returning customers
    returning_customers = insight.get_returning_guests()

    # Showing correlation between room types and cancellations
    # With a plotted crosstab in a heatmap, crosstab because it will allow us to view
    # The frequency distribution between the two columns

    columns = ["assigned_room_type"]
    cont_tbl = insight.correlation_between_columns("is_canceled", columns)
    cont_tbl.plot(kind="bar", rot=90, stacked=True)
    pylt.xlabel('Assigned Room Type')
    pylt.ylabel('Whether the booking is canceled')
    pylt.title('Correlation between the room types and cancellation status')
    cont_tbl.to_excel("cont_table.xlsx", sheet_name="Crosstab Data")
    map_ = maps.heat_map(cont_tbl)
    pylt.show()
