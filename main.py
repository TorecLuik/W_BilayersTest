import argparse
import sys

from process import process


parser = argparse.ArgumentParser(description='Copy input file to output folder')
parser.add_argument('--inputfile', required=True, help='input file')
parser.add_argument('--outputfolder', required=True, help='output folder')
parser.add_argument('--altoutputfolder', help='alternative output folder')
parser.add_argument('--show_progress', action='store_true')
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

result = process(
    args.inputfile,
    args.outputfolder,
    alt_output_folder=args.altoutputfolder,
    show_progress=args.show_progress,
    verbose=args.verbose
)

if result and result != '{}':
    print(result)
    sys.exit(0)
else:
    print('Error')
    sys.exit(1)
