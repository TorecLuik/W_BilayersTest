import json
import os.path
import shutil


def process(input_filename, output_folder, alt_output_folder=None,
            show_progress=False, verbose=False, max_attempts=1, **kwargs):

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

    return json.dumps([result])
