import argparse
import json
import logging
import time

from bdsTx.handlers.satellite_handler import satelliteHandler
from bdsTx.satellite_info.broadcast_type import SIGNAL_TYPE


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Beidou Satellite Navigation Information."
    )
    parser.add_argument(
        "-p",
        "--pos",
        type=float,
        nargs=3,
        help="Position to set, consisting of (longitude, latitude, height).",
    )
    parser.add_argument("-a", "--alc", type=str, help="Path to Almanac file.")
    parser.add_argument("-e", "--eph", type=str, help="Path to Ephemeris file.")
    parser.add_argument(
        "-t", "--time", type=float, default=time.time(), help="Simulation start time."
    )
    parser.add_argument(
        "-s",
        "--signal_type",
        type=str,
        default="B1I",
        help="Signal type, default is `B1I`.",
    )
    parser.add_argument(
        "-i", "--iono_path", type=str, help="Path to ionosphere correction data."
    )
    parser.add_argument(
        "-r", "--prn_path", type=str, help="Path to PRN file directory."
    )
    parser.add_argument("-b", "--broadcast_time", type=float, help="Broadcast time.")
    parser.add_argument("-l", "--ldpc_path", type=str, help="Path to LDPC file.")
    parser.add_argument("-o", "--output", type=str, help="Output file path.")

    return parser.parse_args()


def main():
    args = parse_args()
    print(args)
    logging.basicConfig(level=logging.INFO)
    handler = satelliteHandler()
    handler.set_alc_path(args.alc)
    handler.set_eph_path(args.eph)
    handler.set_time(args.time)
    handler.set_position(args.pos)
    handler.set_broadcast_time(args.broadcast_time)
    handler.set_iono_path(args.iono_path)
    handler.set_prn_path(args.prn_path)
    match args.signal_type:
        case "B1I":
            handler.set_signal_type(SIGNAL_TYPE.B1I_SIGNAL)
        case "B1C":
            handler.set_signal_type(SIGNAL_TYPE.B1C_SIGNAL)
        case _:
            print("invalid signal!")
            return
    if args.ldpc_path:
        handler.set_ldpc_path(args.ldpc_path)
    handler.load_alc().load_eph().load_iono_corr().load_prn()
    if args.ldpc_path:
        handler.load_ldpc_mats()
    handler.find_satellite()
    handler.init_msg_gen()
    msg = handler.generate()
    logging.info("Done.")
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(msg, f, indent=4)


if __name__ == "__main__":
    main()
