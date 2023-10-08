import great_expectations as gx
from great_expectations.checkpoint import Checkpoint
from load_data import PG_CONN_STRING


# Create a context
context = gx.get_context()


# Set up a data source and data asset
pg_datasource = context.sources.add_sql(
    name="pg_datasource", connection_string=PG_CONN_STRING
)

pg_datasource.add_table_asset(name="taxi_data", table_name="taxi_data")

batch_request = pg_datasource.get_asset("taxi_data").build_batch_request()

# Create expectation suite (basically a bundle of expectations)
expectation_suite = "expectations_taxi_data"
context.add_or_update_expectation_suite(expectation_suite_name=expectation_suite)

# Create a validator
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name=expectation_suite,
)

# Add expectations to the validator
validator.expect_column_values_to_not_be_null(column="passenger_count")
validator.expect_column_values_to_be_between(
    column="congestion_surcharge", min_value=0, max_value=1000
)
validator.expect_column_mean_to_be_between(
    column="trip_distance", min_value=3, max_value=5
)


validator.save_expectation_suite(discard_failed_expectations=False)


# Create a checkpoint
taxi_checkpoint = "taxi_checkpoint"

checkpoint = Checkpoint(
    name=taxi_checkpoint,
    run_name_template="%Y%m%d-%H%M%S-my-run-name-template",
    data_context=context,
    batch_request=batch_request,
    expectation_suite_name=expectation_suite,
    action_list=[
        {
            "name": "store_validation_result",
            "action": {"class_name": "StoreValidationResultAction"},
        },
        {
            "name": "update_data_docs",
            "action": {"class_name": "UpdateDataDocsAction"},
        },
    ],
)

context.add_or_update_checkpoint(checkpoint=checkpoint)

# Run a checkpoint
checkpoint_result = checkpoint.run()
# print(context.get_docs_sites_urls())

