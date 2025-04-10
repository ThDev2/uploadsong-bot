<?php
// uploadsong.php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

$host = "localhost";
$user = "YOUR_DB_USER";
$pass = "YOUR_DB_PASS";
$db   = "YOUR_DB_NAME";

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    die(json_encode(["status" => "error", "message" => "DB connection failed"]));
}

$song_id = $_POST["song_id"];
$title = $_POST["title"];
$author = $_POST["author"];
$youtube_url = $_POST["youtube_url"];
$uploader = $_POST["uploader"];
$gdps_link = $_POST["gdps_link"];

$stmt = $conn->prepare("INSERT INTO custom_songs (song_id, title, author, youtube_url, uploader, gdps_link) VALUES (?, ?, ?, ?, ?, ?)");
$stmt->bind_param("isssss", $song_id, $title, $author, $youtube_url, $uploader, $gdps_link);
$stmt->execute();

echo json_encode(["status" => "success", "song_id" => $song_id]);
?>