<?php

$VERSION = "0.0.1";

if (count($argv) < 2) {
  echo "Invalid arguments";
  exit(-1);
}

if ($argv[1] == "--version") {
  echo $VERSION;
  exit(0);
}

if ($argv[1] == "decode") {
    echo json_encode(array(
        "output" => print_r(unserialize(base64_decode($argv[2])), true),
        "read-only" => true,
        "format" => "plain_text",
    ));
} elseif ($argv[1] == "validate") {
    echo json_encode(array(
        "valid" => unserialize(base64_decode($argv[2])) !== false,
        "message" => "",
    ));
}
