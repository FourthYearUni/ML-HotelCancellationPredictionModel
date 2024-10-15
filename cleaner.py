"""
@brief:
This module is responsible for cleaning the data.
It will remove any inconsistencies in the data and make it ready for analysis.
@author: Alain Mugisha(U2083264)

"""

import pandas as pd
from pydantic import BaseModel, ValidationError
from pandas import DataFrame
import calendar


class Booking(BaseModel):
    """
    This class is the base class modeled based on the data in the csv file.
    """

    hotel: str
    is_canceled: int
    lead_time: int
    arrival_date_year: int
    arrival_date_month: str
    arrival_date_week_number: int
    arrival_date_day_of_month: int
    stays_in_weekend_nights: int
    stays_in_week_nights: int
    adults: int
    children: int
    babies: int
    meal: str
    country: str
    market_segment: str
    distribution_channel: str
    is_repeated_guest: int
    previous_cancellations: int
    previous_bookings_not_canceled: int
    reserved_room_type: str
    assigned_room_type: str
    booking_changes: int
    deposit_type: str
    agent: int
    company: int
    days_in_waiting_list: int
    customer_type: str
    adr: float
    required_car_parking_spaces: int
    total_of_special_requests: int
    reservation_status: str
    reservation_status_date: str


class Cleaner:
    """
    This is class has as purpose to define and use all multiple classes.
    """

    def __init__(self):
        self.data_frame: DataFrame = pd.read_csv("hotel_bookings.csv")
        months = list(calendar.month_name)[1:]

        """
        Variable alterations
        """
        # Conversion to number format for easy graphical representation
        self.data_frame["arrival_date_month"] = self.data_frame[
            "arrival_date_month"
        ].map(lambda m: months.index(m) + 1)

        self.data_frame["arrival_date_year"] = self.data_frame["arrival_date_year"].map(
            lambda y: str(y).split("20")[1]
        )
        # This was joined to give more context on date sensitive answers.
        self.data_frame["YearMonth"] = (
            self.data_frame["arrival_date_year"].astype(str)
            + "/"
            + self.data_frame["arrival_date_month"].astype(str)
        )

        # This is to be able to use the duration.
        self.data_frame["duration"] = (
            self.data_frame["stays_in_weekend_nights"]
            + self.data_frame["stays_in_week_nights"]
        )
        self.data_frame = pd.get_dummies(
            self.data_frame,
            columns=[
                "customer_type",
                "assigned_room_type",
                "deposit_type",
                "reservation_status",
                "meal",
                "hotel",
                "arrival_date_month",
                "country",
                "market_segment",
                "distribution_channel",
                "reserved_room_type",
                "reservation_status_date",
                "YearMonth",
            ],
        )

        # print(relevant_f)

    def validate_row(self, row) -> Booking | None:
        """
        Validates each row in the dataframe against the Booking class.
        """
        try:
            booking = Booking(**row.to_dict())
            return booking
        except ValidationError as error:
            print(f"Error validating row: {error}")
            return None

    def validate_data(self) -> DataFrame:
        """
        Validates the whole frame and returns a valid data frame cleaned up.
        """
        # Perform a fill based on the mean value
        self.data_frame["children"] = self.data_frame["children"].fillna(
            self.data_frame.groupby("children")["children"].transform("mean")
        )

        # Perform a text filling as the datatype is text
        self.data_frame["country"] = self.data_frame["country"].fillna("N/A")

        # Perform a backward fill to allow data at the top to be filled
        self.data_frame["agent"] = self.data_frame["agent"].bfill()
        self.data_frame["company"] = self.data_frame["company"].bfill()

        # Perform a backward fill to allow data from the bottom to be filled
        self.data_frame["agent"] = self.data_frame["agent"].ffill()
        self.data_frame["company"] = self.data_frame["company"].ffill()

        dropped = self.data_frame.dropna()
        valid_series = dropped.apply(self.validate_row, axis=1)
        valid_df = DataFrame([booking.dict() for booking in valid_series])
        return valid_df


if __name__ == "__main__":
    cleaner = Cleaner()
    cleaner.validate_data()
    # print(cleaner.validate_data())
