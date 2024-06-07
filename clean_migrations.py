import os
import glob

def find_base_directory():
    current_dir = os.getcwd()
    while True:
        if 'manage.py' in os.listdir(current_dir):
            return current_dir
        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise FileNotFoundError("Could not find the base directory containing 'manage.py'")
        current_dir = parent_dir

def delete_migration_files(base_dir):
    for root, dirs, files in os.walk(base_dir):
        # Skip any directories that contain '.venv' in their path
        if '.venv' in root:
            continue
        if 'migrations' in dirs:
            migrations_dir = os.path.join(root, 'migrations')
            migration_files = glob.glob(os.path.join(migrations_dir, '*.py'))
            for file_path in migration_files:
                if not file_path.endswith('__init__.py'):
                    try:
                        print(f'Deleting {file_path}')
                        os.remove(file_path)
                    except Exception as e:
                        print(f'Failed to delete {file_path}: {e}')

if __name__ == "__main__":
    try:
        base_dir = find_base_directory()
        delete_migration_files(base_dir)
    except Exception as e:
        print(f'Error: {e}')
