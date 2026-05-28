import json
import os.path
import shutil


def _has_allowed_extension(path, allowed_extensions):
    """Return True when file extension matches allowed_extensions."""
    if not allowed_extensions:
        return True
    ext = os.path.splitext(path)[1].lstrip('.').lower()
    normalised = {e.lstrip('.').lower() for e in allowed_extensions if e}
    return ext in normalised


def _copy_path_to_output(src, output_folder, label, allowed_extensions=None):
    """Copy file(s) from a file path or directory into output_folder."""
    if not src:
        return []

    copied = []
    if os.path.isfile(src):
        if not _has_allowed_extension(src, allowed_extensions):
            print(
                f'[{label}] WARNING: skipped {src}; unsupported extension '
                f'for this parameter'
            )
            return []
        dest = os.path.join(output_folder, os.path.basename(src))
        shutil.copy2(src, dest)
        print(f'[{label}] copied {src} -> {dest}')
        return [dest]

    if os.path.isdir(src):
        for name in sorted(os.listdir(src)):
            file_path = os.path.join(src, name)
            if not os.path.isfile(file_path):
                continue
            if not _has_allowed_extension(file_path, allowed_extensions):
                continue
            dest = os.path.join(output_folder, name)
            shutil.copy2(file_path, dest)
            copied.append(dest)
            print(f'[{label}] copied {file_path} -> {dest}')
        if copied:
            return copied
        print(
            f'[{label}] WARNING: no matching files found in directory: '
            f'{src}'
        )
        return []

    print(f'[{label}] WARNING: file or directory not found: {src}')
    return []


def _is_subpath(child, parent):
    """Return True if child is the same as, or a subdirectory of, parent."""
    try:
        child_abs = os.path.realpath(os.path.abspath(child))
        parent_abs = os.path.realpath(os.path.abspath(parent))
        return (
            child_abs == parent_abs
            or child_abs.startswith(parent_abs + os.sep)
        )
    except (ValueError, TypeError):
        return False


def _resolve_logfile_paths(logfile):
    """Resolve one or more logfile paths from a file or directory input."""
    if not logfile:
        return []

    # Some runners pass logfile as an output directory.
    # In that case, use any existing .log files in that directory.
    if os.path.isdir(logfile):
        existing_logs = sorted(
            os.path.join(logfile, name)
            for name in os.listdir(logfile)
            if name.lower().endswith('.log')
            and os.path.isfile(os.path.join(logfile, name))
        )
        if existing_logs:
            return existing_logs
        return [os.path.join(logfile, 'run.log')]

    base = os.path.basename(logfile)
    ext = os.path.splitext(base)[1]
    if not ext:
        # Treat extension-less values as a directory path.
        if os.path.exists(logfile):
            existing_logs = sorted(
                os.path.join(logfile, name)
                for name in os.listdir(logfile)
                if name.lower().endswith('.log')
                and os.path.isfile(os.path.join(logfile, name))
            )
            if existing_logs:
                return existing_logs
        return [os.path.join(logfile, 'run.log')]

    return [logfile]


def process(input_filename, output_folder, alt_output_folder=None,
            show_progress=False, verbose=False, max_attempts=1,
            pick_one='alpha', a_number=1.0, an_axis=0, a_count=10,
            logfile='', measurement_table_dir=None,
            extra_array=None, config_file=None, custom_model=None, **kwargs):

    print(
        f'[params] pick_one={pick_one!r} a_number={a_number} '
        f'an_axis={an_axis} a_count={a_count}'
    )

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

    attachment_params = [
        (
            'measurement_table', measurement_table_dir,
            {'csv', 'parquet', 'feather'}, None, 'measurement_tables'
        ),
        (
            'extra_array', extra_array,
            {'npy', 'npz'}, 'extra_array', 'extra_array_files'
        ),
        (
            'config_file', config_file,
            {'json', 'yaml', 'yml', 'toml'}, 'config_file', 'config_files'
        ),
        (
            'custom_model', custom_model,
            None, 'custom_model', 'custom_model_files'
        ),
    ]
    copied_attachments = {}
    for param, src, formats, single_key, multi_key in attachment_params:
        if src and os.path.isdir(src) and _is_subpath(src, input_filename):
            # This attachment dir is already under input_filename, so copytree
            # above has already placed it in the output.  Don't copy again.
            print(
                f'[{param}] skipping copy of {src!r} '
                f'(already under {input_filename!r}, covered by copytree)'
            )
            copied_attachments[param] = []
            continue
        copied_paths = _copy_path_to_output(
            src,
            output_folder,
            param if param != 'measurement_table' else 'table',
            formats,
        )
        copied_attachments[param] = copied_paths
        if not copied_paths:
            continue
        if single_key:
            result[single_key] = copied_paths[0]
        if multi_key and (
            param == 'measurement_table' or len(copied_paths) > 1
        ):
            result[multi_key] = copied_paths

    resolved_logfiles = _resolve_logfile_paths(logfile)
    if resolved_logfiles:
        for resolved_logfile in resolved_logfiles:
            logdir = os.path.dirname(resolved_logfile)
            if logdir:
                os.makedirs(logdir, exist_ok=True)
            with open(resolved_logfile, 'a') as f:
                f.write(f'pick_one={pick_one}\n')
                f.write(f'a_number={a_number}\n')
                f.write(f'an_axis={an_axis}\n')
                f.write(f'a_count={a_count}\n')
                f.write(f'input={input_filename}\n')
                f.write(f'output={output_path}\n')
                for param, paths in copied_attachments.items():
                    for i, path in enumerate(paths):
                        f.write(f'{param}_{i}={path}\n')
                f.write('\n')
        result['logfile'] = resolved_logfiles[0]
        if len(resolved_logfiles) > 1:
            result['logfiles'] = resolved_logfiles

    return json.dumps([result])
