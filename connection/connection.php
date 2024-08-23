<?php
$hostname = "localhost";
$username = "root";
$password = "saurabh16";
$dbname = "project2";

function connectToDatabase() {
    global $hostname, $username, $password, $dbname;
    $conn = new mysqli($hostname, $username, $password, $dbname);

    if ($conn->connect_error) {
        die("Connection failed: " . $conn->connect_error);
    }

    return $conn;
}

// Call the function to establish the connection
$conn = connectToDatabase();
?>
