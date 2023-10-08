from sqlalchemy import create_engine
import pandas as pd


PATH_TO_DATA = (
    "/workspaces/demo-great-expectations" "/data/yellow_tripdata_sample_2019-01.csv"
)

PG_CONN_STRING = "postgresql+psycopg2://" "postgres:password@postgres:5432/postgres"


engine = create_engine(PG_CONN_STRING)


def load_data():
    df = pd.read_csv(PATH_TO_DATA, sep=",")
    df.to_sql("taxi_data", con=engine, index=False)


if __name__ == "__main__":
    load_data()
