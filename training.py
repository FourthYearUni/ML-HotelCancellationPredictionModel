"""
@brief:
Provides training functionality for the cleaned and prepared
data presented as a dataframe
"""

from pandas.core.common import random_state
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from cleaner import Cleaner


class Train:
    """
    Provides methods to facilitate the training
    """

    def __init__(self) -> None:
        """
        Base constructor, setting up class properties
        """
        self.data_frame = Cleaner().data_frame

    def split(self):
        """
        Splits the dataset into features and labels
        """
        # print(self.data_frame.columns)
        x = self.data_frame[
            [
                "stays_in_week_nights",
                "stays_in_weekend_nights",
                "previous_cancellations",
                "previous_bookings_not_canceled",
                "booking_changes",
                "days_in_waiting_list",
                "is_repeated_guest",
                "lead_time",
                "deposit_type_Non Refund",
                "adr",
                "assigned_room_type_A",
                "agent",
                "customer_type_Transient",
                "market_segment_Groups",
                "country_PRT",
                "hotel_City Hotel",
                "hotel_Resort Hotel",
                "meal_FB",
            ]
        ]
        y = self.data_frame["reservation_status_Canceled"]
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3, random_state=42
        )

        return (x_train, x_test, y_train, y_test)

    def train(self):
        """
        Method for training the dataset using RandomForestClassifier
        """
        x_train, x_test, y_train, y_test = self.split()
        rf = RandomForestClassifier(n_estimators=100, random_state=42)

        rf.fit(x_train, y_train)

        y_pred = rf.predict(x_test)

        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy: {accuracy: .2f}")


if __name__ == "__main__":
    train = Train()
    train.train()
