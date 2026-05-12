import argparse


parser = argparse.ArgumentParser(description='Convert file to ome format')
parser.add_argument('--inputfile', required=True, help='input file')
parser.add_argument('--outputfolder', required=True, help='output folder')
parser.add_argument('--altoutputfolder', help='alternative output folder')
parser.add_argument('--outputformat', help='output format version', default='omezarr2')
parser.add_argument('--show_progress', action='store_true')
parser.add_argument('--verbose', action='store_true')
# Allow additional arguments for source-specific parameters (e.g., --plateid)
parser.add_argument('--plateid', help='Incucyte plate ID (optional)')
args = parser.parse_args()

result = process(
    args.inputfile,
    args.outputfolder,
    alt_output_folder=args.altoutputfolder,
    output_format=args.outputformat,
    show_progress=args.show_progress,
    verbose=args.verbose
)

if result and result != '{}':
    print(result)
    sys.exit(0)
else:
    print('Error')
    sys.exit(1)
