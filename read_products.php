<?php
include "config.php";

/* ---------- Headers ---------- */
header("Content-Type: application/json; charset=UTF-8");
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Methods: GET");
header("Access-Control-Allow-Headers: Content-Type, Authorization");

/* ---------- Base URL ---------- */
$baseUrl = "http://localhost/shoppingai/uploads/";

/* ---------- Query ---------- */
$sql = "SELECT 
    product_id,
    product_image,
    product_name,
    product_category,
    product_description,
    color,
    size,
    gender,
    price,
    stock,
    quantity,
    created_at
FROM clothing
ORDER BY product_id DESC";

$result = mysqli_query($conn, $sql);

/* ---------- Response ---------- */
$response = [
    "status" => false,
    "message" => "No products found",
    "count" => 0,
    "data" => []
];

if ($result && mysqli_num_rows($result) > 0) {

    while ($row = mysqli_fetch_assoc($result)) {

        $image = $row["product_image"];

        // ✅ Prevent duplicate base URL
        if (!empty($image)) {
            if (filter_var($image, FILTER_VALIDATE_URL)) {
                $imageUrl = $image; // already full URL
            } else {
                $imageUrl = $baseUrl . $image; // filename only
            }
        } else {
            $imageUrl = null;
        }

        $response["data"][] = [
            "product_id" => $row["product_id"],
            "product_image" => $imageUrl,
            "product_name" => $row["product_name"],
            "product_category" => $row["product_category"],
            "product_description" => $row["product_description"],
            "color" => $row["color"],
            "size" => $row["size"],
            "gender" => $row["gender"],
            "price" => $row["price"],
            "stock" => $row["stock"],
            "quantity" => $row["quantity"],
            "created_at" => $row["created_at"]
        ];
    }

    $response["status"] = true;
    $response["message"] = "Products fetched successfully";
    $response["count"] = count($response["data"]);
}

/* ---------- Output ---------- */
echo json_encode($response, JSON_PRETTY_PRINT);
mysqli_close($conn);
?>
