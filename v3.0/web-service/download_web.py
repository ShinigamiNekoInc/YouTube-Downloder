import os
import sys
import io
import json
from yt_dlp import YoutubeDL

# Force output to handle UTF-8 characters correctly on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def update_task_status(task_id: str, status: str, extra_data: dict = None):
    tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
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

def download_best_video(url: str, output_dir: str = './downloads', task_id: str = None):
    os.makedirs(output_dir, exist_ok=True)
    
    if task_id:
        update_task_status(task_id, "started")

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'merge_output_format': 'mkv',
        # Path to ffmpeg.exe folder (replace with your path!)
        'ffmpeg_location': os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg', 'bin'),
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            print(f"STARTING_DOWNLOAD_PROGRESS: {url}")
            info = ydl.extract_info(url, download=True)
            # Get the filename from the info dictionary
            filename = ydl.prepare_filename(info)
            
            if task_id:
                update_task_status(task_id, "completed", {"filename": filename})
            print(f"FINISHED_DOWNLOAD_PATH: {filename}")
    except Exception as e:
        error_msg = str(e)
        print(f'Error occurred: {error_msg}')
        if task_id:
            update_task_status(task_id, "error", {"message": error_msg})
        sys.exit(1)
    finally:
        # Cleanup the task file after finishing or failing
        if task_id:
            tasks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tasks')
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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python download_web.py <url> <output_dir> [task_id]")
        sys.exit(1)
    
    video_url = sys.argv[1].strip()
    out_dir = sys.argv[2] if len(sys.argv) > 3 else './downloads'
    # In the new flow, out_dir might be passed as a path and task_id as the third arg
    # However, based on current script structure: url, output_dir, then optionally task_id
    task_id = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not out_dir.startswith(os.path.abspath(os.getcwd())) and not out_dir.startswith(os.path.abspath(os.path.dirname(__file__))):
        # If the provided out_dir is relative, make it absolute based on current script dir to be safe
        out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), out_dir))

    download_best_video(video_url, out_dir, task_id)