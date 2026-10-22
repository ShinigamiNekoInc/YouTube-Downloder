<?php
// Configuration
$downloads_dir = __DIR__ . '/../downloads';

if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['file'])) {
    $filename = basename($_GET['file']); // Use basename to prevent directory traversal attacks
    $file_path = $downloads_dir . '/' . $filename;

    if (file_exists($file_path) && is_file($file_path)) {
        // Clear any previous output buffers
        while (ob_get_level()) {
            ob_end_clean();
        }

        $file_size = filesize($file_path);
        $mime_type = 'video/x-matroska'; // Default for .mkv

        // Set headers for streaming large files
        header('Content-Type: ' . $mime_type);
        header('Content-Disposition: attachment; filename="' . $filename . '"');
        header('Content-Transfer-Encoding: binary');
        header('Content-Length: ' . $file_size);
        header('Cache-Control: no-cache, must-revalidate');
        header('Pragma: no-cache');
        header('Expires: 0');

        // Stream the file efficiently
        readfile($file_path);
        exit;
    } else {
        header("HTTP/1.0 404 Not Found");
        echo "File not found.";
        exit;
    }
} else {
    header("HTTP/1.0 400 Bad Request");
    echo "Invalid request.";
    exit;
}