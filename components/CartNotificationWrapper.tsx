"use client";

import React from "react";
import { useCart } from "../context/CartContext";
import CartNotification from "./CartNotification";

export default function CartNotificationWrapper() {
  const { showNotification, lastAddedProduct, hideNotification } = useCart();

  return (
    <CartNotification
      show={showNotification}
      productName={lastAddedProduct}
      onHide={hideNotification}
    />
  );
}