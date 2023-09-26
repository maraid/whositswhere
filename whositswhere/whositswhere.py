import argparse
import builder
from datetime import datetime
import graphics
import json
import logging
import os
import pathlib
import pickle
import queries
import sys


ROOT_DIR = pathlib.Path(__file__).parents[1].resolve()
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.json"
DEFAULT_RESULTS_PATH = ROOT_DIR / "results"


def load_config(config_path):
    with open(config_path, "r", encoding="utf-8") as f:
        return json.loads(f.read())


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    parser = argparse.ArgumentParser("Who Sits Where In The Office")
    parser.add_argument(
        "date",
        help="Run on a specified date. format: YYYY-MM-DD",
        default=datetime.today().strftime(r"%Y-%m-%d"),
        nargs="?")
    parser.add_argument(
        "-c", "--config",
        help="Specify path to config file",
        default=DEFAULT_CONFIG_PATH,
        metavar="<path>")
    parser.add_argument(
        "-r", "--result",
        help="Directory to put the generated images",
        default=DEFAULT_RESULTS_PATH,
        metavar="<path>")
    args = parser.parse_args()

    config = load_config(args.config)
    logging.info("Config loaded")

    session = queries.ParkanizerSession(config["username"], config["password"])

    logging.info(f"Creating reservation map. Selected date: {args.date}")
    rmb = builder.ReservationMapBuilder(session, args.date)
    zones = rmb.build()

    # with open("zones.pickle", "wb") as f:
    #     pickle.dump(zones, f)
    #
    # with open("zones.pickle", "rb") as f:
    #     zones = pickle.load(f)

    logging.info("Creating Images for the fetched zones")
    args.result.mkdir(exist_ok=True)
    img_handler = graphics.ImageHandler(session, zones, config["vip"])
    img_handler.create_images(args.result)

    logging.info(f"Opening result location: {args.result}")
    if sys.platform.startswith("win"):
        os.startfile(args.result)


if __name__ == "__main__":
    main()
