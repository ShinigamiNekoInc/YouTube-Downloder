<?php
require_once __DIR__ . '/config.php';

$dir = __DIR__ . '/../downloads';

function get_dir_size($path) {
    $size = 0;
    if (is_dir($path)) {
        $files = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($path, RecursiveDirectoryIterator::SKIP_DOTS),
            RecursiveIteratorIterator::CHILD_FIRST
        );
        foreach ($files as $file) {
            $size += $file->getSize();
        }
    }
    return $size;
}

$size = get_dir_size($dir);
header('Content-Type: application/json');
echo json_encode(['bytes' => $size]);