"""
@brief:
This module is responsible for cleaning the data.
It will remove any inconsistencies in the data and make it ready for analysis.
@author: Alain Mugisha(U2083264)

"""
from datetime import datetime

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
    reservation_status_date: datetime


class Cleaner:
    """
    This is class has as purpose to define and use all multiple classes.
    """

    def __init__(self):
        self.data_frame: DataFrame = pd.read_csv("hotel_bookings.csv")

    @staticmethod
    def validate_row(row) -> Booking | None:
        """
        Validates each row in the dataframe against the Booking class.
        """
        try:
            booking = Booking(**row.to_dict())
            return booking
        except ValidationError as error:
            print(f"Error validating row: {error}")
            return None

    @staticmethod
    def drop_columns(df: DataFrame) -> DataFrame:
        """
        Removes columns from the data frame that are not needed
        """
        data_frame = df.drop(columns=[
            'agent',
            'company',
            'required_car_parking_spaces',
            'distribution_channel',
        ], axis=1)
        return data_frame

    @staticmethod
    def drop_invalid_rows(df: DataFrame) -> DataFrame:
        """
        Drops rows that contain values that is inconsistent.
        """
        # Drops rows where total number of days is zero and the booking is not cancelled
        invalid_stay = df.query(
            "stays_in_weekend_nights == 0 and stays_in_week_nights == 0 and is_canceled == 0"
        )
        df.drop(invalid_stay, axis=1, inplace=True)
        return df

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

        dropped = self.data_frame.dropna()
        valid_series = dropped.apply(self.validate_row, axis=1)
        valid_df = DataFrame([booking.dict() for booking in valid_series])

        # Run the dataframe through an extra series of cleaning functions
        # Dropping invalid columns
        #valid_clean_df = self.drop_columns(valid_df)

        # Dropping rows with inconsistent data
        #valid_clean_df = self.drop_invalid_rows(valid_clean_df)

        return valid_df


if __name__ == "__main__":
    cleaner = Cleaner()
    cleaner.validate_data()
    print(cleaner.validate_data())
