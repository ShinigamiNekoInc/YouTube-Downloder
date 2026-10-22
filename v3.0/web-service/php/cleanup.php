<?php
require_once __DIR__ . '/config.php';

$cleanupScript = $baseDir . '\python\cleanup.py';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Generate a unique Task ID for the cleanup process
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

    // Execute the cleanup script in background on Windows with the task ID
    $command = "start /B \"\" $pythonPath $cleanupScript $task_id > nul 2>&1";
    pclose(popen($command, "r"));

    // Redirect to index.html so frontend can start polling for completion
    header("Location: ./../index.html?type=cleanup_started&task_id=" . urlencode($task_id));
    exit;
} else {
    header("Location: ./../index.html");
    exit;
}