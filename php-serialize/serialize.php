<?php
$VERSION = "0.0.2";

if (count($argv) < 2) {
    echo json_encode(array('error' => "Invalid arguments"));
    exit(1);
}

switch ($argv[1]) {
case 'info':
    $data = array(
        'version' => $VERSION,
        'description' => 'PHP serialize formatter'
    );
    break;

case 'validate':
    $data = array(
        "valid" => @unserialize(base64_decode($argv[2])) !== false,
        "error" => error_get_last(),
    );
    break;

case 'decode':
    $data = array(
        "output" => print_r(unserialize(base64_decode($argv[2])), true),
        "read-only" => true,
        "format" => "plain_text",
    );
    break;

default:
    $data = array();
}

echo json_encode($data);
