import argparse
import sys

from process import process


parser = argparse.ArgumentParser(description='Copy input file to output folder')
parser.add_argument('--inputfile', required=True, help='input file')
parser.add_argument('--outputfolder', required=True, help='output folder')
parser.add_argument('--altoutputfolder', help='alternative output folder')
parser.add_argument('--measurement_table', default=None, help='directory containing measurement/table files to pass through')
parser.add_argument('--extra_array', default=None, help='path to numpy array file (.npy/.npz) to pass through')
parser.add_argument('--config_file', default=None, help='path to config/parameter file to pass through')
parser.add_argument('--custom_model', default=None, help='path to model weights or executable to pass through')
parser.add_argument('--show_progress', action='store_true')
parser.add_argument('--verbose', action='store_true')
# Parameters
parser.add_argument('--pick_one', default='alpha',
                    choices=['alpha', 'beta', 'gamma'])
parser.add_argument('--a_number', type=float, default=1.0)
parser.add_argument('--an_axis', type=int, default=0)
parser.add_argument('--a_count', type=int, default=10)
parser.add_argument('--savedir', default='/output_images')
# Outputs
parser.add_argument('--logfile', default='', help='path to write run log')
args = parser.parse_args()

result = process(
    args.inputfile,
    args.outputfolder,
    alt_output_folder=args.altoutputfolder,
    show_progress=args.show_progress,
    verbose=args.verbose,
    pick_one=args.pick_one,
    a_number=args.a_number,
    an_axis=args.an_axis,
    a_count=args.a_count,
    logfile=args.logfile,
    measurement_table_dir=args.measurement_table,
    extra_array=args.extra_array,
    config_file=args.config_file,
    custom_model=args.custom_model,
)

if result and result != '{}':
    print(result)
    sys.exit(0)
else:
    print('Error')
    sys.exit(1)
