import json
import os.path
import shutil


def process(input_filename, output_folder, alt_output_folder=None,
            show_progress=False, verbose=False, max_attempts=1,
            pick_one='alpha', a_number=1.0, an_axis=0, a_count=10,
            logfile='', **kwargs):

    print(f'[params] pick_one={pick_one!r} a_number={a_number} an_axis={an_axis} a_count={a_count}')

    filename = os.path.basename(input_filename)
    title = os.path.splitext(filename)[0].rstrip('.ome')
    result = {'name': title}

    output_path = os.path.join(output_folder, filename)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    shutil.copytree(input_filename, output_path, dirs_exist_ok=True)
    result['full_path'] = output_path
    message = f'Exported   {output_path}'

    if alt_output_folder:
        alt_output_path = os.path.join(alt_output_folder, filename)
        if not os.path.exists(alt_output_folder):
            os.makedirs(alt_output_folder)
        shutil.copytree(input_filename, alt_output_path, dirs_exist_ok=True)
        result['alt_path'] = alt_output_path
        message += f' and {alt_output_path}'

    if show_progress:
        print(message)

    if logfile:
        os.makedirs(os.path.dirname(logfile), exist_ok=True) if os.path.dirname(logfile) else None
        with open(logfile, 'w') as f:
            f.write(f'pick_one={pick_one}\n')
            f.write(f'a_number={a_number}\n')
            f.write(f'an_axis={an_axis}\n')
            f.write(f'a_count={a_count}\n')
            f.write(f'input={input_filename}\n')
            f.write(f'output={output_path}\n')
        result['logfile'] = logfile

    return json.dumps([result])
