<?php
include "config.php";

if ($_SERVER["REQUEST_METHOD"] == "POST") {

    $product_name = $_POST['product_name'];
    $product_category = $_POST['product_category'];
    $product_description = $_POST['product_description'];
    $color = $_POST['color'];
    $size = $_POST['size'];
    $gender = $_POST['gender'];
    $price = $_POST['price'];
    $stock = $_POST['stock'];
    $quantity = $_POST['quantity'];

    /* ---------- Image Upload ---------- */
    $image_name = time() . "_" . $_FILES['product_image']['name']; // unique name
    $image_tmp  = $_FILES['product_image']['tmp_name'];
    $upload_dir = "uploads/";
    $upload_path = $upload_dir . $image_name;

    // Base URL
    $base_url = "http://localhost/shoppingai/";
    $image_url = $base_url . $upload_path;

    if (move_uploaded_file($image_tmp, $upload_path)) {

        $sql = "INSERT INTO clothing 
        (product_image, product_name, product_category, product_description, color, size, gender, price, stock, quantity)
        VALUES 
        ('$image_url', '$product_name', '$product_category', '$product_description', '$color', '$size', '$gender', '$price', '$stock', '$quantity')";

        if (mysqli_query($conn, $sql)) {
            echo "Product uploaded successfully";
        } else {
            echo "Database error: " . mysqli_error($conn);
        }

    } else {
        echo "Image upload failed";
    }
}
?>
