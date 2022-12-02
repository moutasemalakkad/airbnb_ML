#!/usr/bin/env python
"""
input_artifact,output_artifact,output_type,output_description,min_price,max_price
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info("Downloading data from W&B")

    artifact_local_path = run.use_artifact(args.input_artifact).file()
    # Drop outliers
    df = pd.read_csv(artifact_local_path)
    min_price = 10
    max_price = 350
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("DONE: data cleaned")

    logger.info(f"saving cleaned data: {args.output_artifact}")

    df.to_csv(args.output_artifact, index=False)

    logger.info(f"DONE: saved csv: {args.output_artifact}")

    logger.info(f"uploading artifact to W&B: {args.output_artifact}")

    artifact = wandb.Artifact(args.output_artifact, type=args.output_type, description=args.output_description)
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="name of the input artficate",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="name of the output artficate",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="output type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="output description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
