import json
import os.path
import shutil


def _copy_file_to_output(src, output_folder, label):
    """Copy a single file to output_folder. Returns dest path or None."""
    if not src:
        return None
    if os.path.isfile(src):
        dest = os.path.join(output_folder, os.path.basename(src))
        shutil.copy2(src, dest)
        print(f'[{label}] copied {src} -> {dest}')
        return dest
    print(f'[{label}] WARNING: file not found: {src}')
    return None


def process(input_filename, output_folder, alt_output_folder=None,
            show_progress=False, verbose=False, max_attempts=1,
            pick_one='alpha', a_number=1.0, an_axis=0, a_count=10,
            logfile='', measurement_table_dir=None,
            extra_array=None, config_file=None, custom_model=None, **kwargs):

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

    # Copy measurement table files to output and track them
    copied_tables = []
    if measurement_table_dir and os.path.isdir(measurement_table_dir):
        for fname in sorted(os.listdir(measurement_table_dir)):
            src = os.path.join(measurement_table_dir, fname)
            if os.path.isfile(src):
                dest = os.path.join(output_folder, fname)
                shutil.copy2(src, dest)
                copied_tables.append(dest)
                print(f'[table] copied {src} -> {dest}')
    elif measurement_table_dir:
        print(f'[table] WARNING: directory not found: {measurement_table_dir}')
    if copied_tables:
        result['measurement_tables'] = copied_tables

    # Copy single-file attachments to output
    copied_extra_array = _copy_file_to_output(extra_array, output_folder, 'extra_array')
    if copied_extra_array:
        result['extra_array'] = copied_extra_array

    copied_config_file = _copy_file_to_output(config_file, output_folder, 'config_file')
    if copied_config_file:
        result['config_file'] = copied_config_file

    copied_custom_model = _copy_file_to_output(custom_model, output_folder, 'custom_model')
    if copied_custom_model:
        result['custom_model'] = copied_custom_model

    if logfile:
        os.makedirs(os.path.dirname(logfile), exist_ok=True) if os.path.dirname(logfile) else None
        with open(logfile, 'w') as f:
            f.write(f'pick_one={pick_one}\n')
            f.write(f'a_number={a_number}\n')
            f.write(f'an_axis={an_axis}\n')
            f.write(f'a_count={a_count}\n')
            f.write(f'input={input_filename}\n')
            f.write(f'output={output_path}\n')
            for i, t in enumerate(copied_tables):
                f.write(f'measurement_table_{i}={t}\n')
            if copied_extra_array:
                f.write(f'extra_array={copied_extra_array}\n')
            if copied_config_file:
                f.write(f'config_file={copied_config_file}\n')
            if copied_custom_model:
                f.write(f'custom_model={copied_custom_model}\n')
        result['logfile'] = logfile

    return json.dumps([result])
