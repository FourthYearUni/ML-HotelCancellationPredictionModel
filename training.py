"""
@brief:
Provides training functionality for the cleaned and prepared
data presented as a dataframe
"""

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from feature_engineering import FeatureEngineering

from cleaner import Cleaner
from plots import Charts


class Train:
    """
    Provides methods to facilitate the training
    """

    def __init__(self) -> None:
        """
        Base constructor, setting up class properties
        """
        self.data_frame = Cleaner().validate_data()
        self.f_eng = FeatureEngineering(data_frame=self.data_frame)

        # Call methods for feature engineering to have the right methods called.
        self.f_eng.create_month_year()
        self.f_eng.create_duration()
        self.data_frame = self.f_eng.one_hot_encoding(
            properties=[
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
            ]
        )
        self.charts = Charts()

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
            x, y, test_size=0.2, random_state=42
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
        return y_test, y_pred

    def evaluate(self, rf, y_test, y_pred):
        """
        Evaluate the model by calculating precision,
        recall f1-score  and plotting a chart
        about feature importance.
        """
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        conf_matx = confusion_matrix(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print("Precision:", precision)
        print("Recall:", recall)
        print("F1-Score:", f1)
        print(f"Accuracy: {accuracy: .2f}")

        roc_auc = roc_auc_score(y_test, y_pred)
        print("AUC-ROC:", roc_auc)

        print("Confusion Matrix: \n", conf_matx)

        impt = rf.feature_importances_
        impt_r = [imp for imp in list(range(len(impt)))]
        chart = self.charts.line_chart(
            impt_r, impt, ["Score", "Feature"], "Feature importance"
        )
        chart.show()


if __name__ == "__main__":
    train = Train()
    train.train()
