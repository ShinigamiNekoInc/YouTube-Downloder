<?php
$tasks_dir = __DIR__ . '/tasks';

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['task_id'])) {
    $task_id = basename($_GET['task_id']); // Prevent directory traversal
    $task_file = $tasks_dir . '/' . $task_id . '.json';

    header('Content-Type: application/json');

    if (file_exists($task_file)) {
        echo file_get_contents($task_file);
    } else {
        http_response_code(404);
        echo json_encode(["status" => "not_found", "message" => "Task not found."]);
    }
    exit;
}

http_response_code(400);
echo json_encode(["status" => "error", "message" => "Invalid request. Task ID required."]);
exit;