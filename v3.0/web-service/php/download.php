<?php
// Configuration
$pythonPath = 'C:\inetpub\libs\pythoncore-3.14-64\python.exe';
$python_script = 'C:\inetpub\wwwroot\projects\youtubedl\download_web.py';
$downloads_dir = __DIR__ . '/../downloads';

// Ensure downloads directory exists
if (!file_exists($downloads_dir)) {
    mkdir($downloads_dir, 0777, true);
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['video_url'])) {
    $video_url = escapeshellarg($_POST['video_url']);
    // Use absolute path for the download directory to ensure python finds it correctly
    $out_dir = escapeshellarg(realpath($downloads_dir));

    // Generate a unique Task ID
    $task_id = uniqid('task_', true);
    $tasks_dir = __DIR__ . '/../tasks';
    if (!file_exists($tasks_dir)) {
        mkdir($tasks_dir, 0777, true);
    }

    // Create initial status file
    $task_file = $tasks_dir . '/' . $task_id . '.json';
    file_put_contents($task_file, json_encode([
        "status" => "queued",
        "updated_at" => date('Y-m-d H:i:s')
    ]));

    // Execute the python script in background on Windows using popen/pclose 
    // to ensure it detaches from the PHP process and doesn't cause timeouts.
    $command = "start /B \"\" $pythonPath $python_script $video_url $out_dir $task_id > nul 2>&1";
    pclose(popen($command, "r"));

    // Redirect to index.html with the Task ID so frontend can start polling
    header("Location: ./../index.html?type=started&task_id=" . urlencode($task_id));
    exit;
} else {
    header("Location: ./../index.html");
    exit;
}