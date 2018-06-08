<?php

$VERSION = '0.0.1';

if ($argc < 2) {
    echo 'Invalid arguments';
    exit(-1);
}

$action = $argv[1];
$value = isset($argv[2]) ? base64_decode($argv[2]) : '';

if ($action === '--version') {
    echo $VERSION;
    exit(0);
}

function is_gzip($value)
{
    return is_string($value) && 0 === strpos($value, "\x1f" . "\x8b" . "\x08");
}

if ($action === 'validate') {
    echo json_encode([
        'valid' => is_gzip($value),
        'message' => '',
    ]);
}

if ($action === 'decode') {
    echo json_encode([
        'output' => is_gzip($value) ? gzdecode($value) : $value,
        'read-only' => true,
        'format' => 'plain_text',
    ]);
}
