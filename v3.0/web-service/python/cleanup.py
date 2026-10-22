import os
import time
import sys

def cleanup_downloads(directory, days=10):
    """
    Removes files in the specified directory that are older than a certain number of days.
    """
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    now = time.time()
    seconds_in_day = 86400
    threshold = now - (days * seconds_in_day)

    print(f"Cleaning up files in {directory} older than {days} days...")
    
    files_removed = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_mod_time = os.path.getmtime(file_path)
            if file_mod_time < threshold:
                try:
                    os.remove(file_path)
                    print(f"Removed: {filename}")
                    files_removed += 1
                except Exception as e:
                    print(f"Error removing {filename}: {e}")

    print(f"Cleanup complete. Removed {files_removed} files.")
    if task_id:
        update_task_status(task_id, "completed")

if __name__ == "__main__":
    # Path relative to this script's directory (v3.0/web-service/python)
    # The downloads folder is at v3.0/web-service/downloads
    base_dir = os.path.abspath(os.path.dirname(__file__))
    downloads_dir = os.path.join(base_dir, '..', 'downloads')
    
    # Get task_id from arguments if provided
    task_id = sys.argv[1] if len(sys.argv) > 1 else None
    
    cleanup_downloads(downloads_dir)
