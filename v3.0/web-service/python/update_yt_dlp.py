import subprocess
import sys
import io
import os
import json
from datetime import datetime

def update_task_status(task_id: str, status: str, extra_data: dict = None):
    tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
    os.makedirs(tasks_dir, exist_ok=True)
    task_file = os.path.join(tasks_dir, f"{task_id}.json")
    
    data = {
        "status": status,
        "updated_at": str(io.datetime.now().strftime('%Y-%m-%d %H:%M:%S')) if hasattr(io, 'datetime') else str(os.times()) # Fallback if datetime not imported
    }
    if extra_data:
        data.update(extra_data)
    
    # For simple status we don't need full datetime logic in every update to keep it fast
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def update_yt_dlp(task_id=None):
    if task_id:
        update_task_status(task_id, "started")

    try:
        # Use the current python executable to run pip
        # This ensures we are updating the library for the correct python environment
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"])
        if task_id:
            update_task_status(task_id, "completed")
        print("SUCCESS: yt-dlp updated successfully.")
    except subprocess.CalledProcessError as e:
        error_msg = str(e)
        if task_id:
            update_task_status(task_id, "error", {"message": error_msg})
        print(f"ERROR: Failed to update yt-dlp. Error: {error_msg}")
        sys.exit(1)
    except Exception as e:
        error_msg = str(e)
        if task_id:
            update_task_status(task_id, "error", {"message": error_msg})
        print(f"ERROR: An unexpected error occurred: {error_msg}")
        sys.exit(1)
    finally:
        # Cleanup the task file after finishing or failing
        if task_id:
            tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks')
            task_file = os.path.join(tasks_dir, f"{task_id}.json")
            if os.path.exists(task_file):
                # Note: If we delete it immediately on completion, the frontend might 
                # fail to see the "completed" status if it polls just after completion.
                # However, since the user wants them removed and they are technically 'finished',
                # I will add a slight delay or handle logic so status is visible before deletion.
                # For this specific request, let's stick to simple removal but ensure 
                # it happens at the very end of the script execution.
                import time
                time.sleep(5) 
                try:
                    os.remove(task_file)
                except Exception:
                    pass

if __name__ == "__main__":
    # Expect task_id as first argument if provided
    tid = sys.argv[1] if len(sys.argv) > 1 else None
    update_yt_dlp(tid)
