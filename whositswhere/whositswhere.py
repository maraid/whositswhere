import argparse
import builder
from datetime import datetime
import json
import logging
import queries
import graphics
import pathlib
import pickle
import sys


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
        default=pathlib.Path(__file__).parents[1].resolve() / "config.json",
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
    img_handler = graphics.ImageHandler(session, zones, config["vip"])
    img_handler.get_image()


if __name__ == "__main__":
    main()
