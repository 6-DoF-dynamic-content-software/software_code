import sys
import time
sys.path.insert(1, './lib')
import objParser
import plyMerge

import argparse
from pathlib import Path

if __name__ == "__main__":
    startTime = time.time()
    # argparser start
    parser = argparse.ArgumentParser()
    parser.add_argument('-jp', '--json_path', dest='json_path',
                        help="Json file")
    parser.add_argument(
        "--skip_objParser",
        dest="skip_objParser",
        action="store_true",
        default=False,
        help="If set, objParser will be skipped",
    )
    parser.add_argument(
        "--skip_plyMerge",
        dest="skip_plyMerge",
        action="store_true",
        default=False,
        help="If set, plyMerge will be skipped",
    )
    args = parser.parse_args()
    # argparser end
    
    jsonFilePath = Path(f"{args.json_path}")
    print(jsonFilePath)
    
    if not args.skip_objParser:
        objParser.main(jsonFilePath)
    if not args.skip_plyMerge:
        plyMerge.main(jsonFilePath, write_ascii=False)
    endTime = time.time()
    print(endTime-startTime)
    