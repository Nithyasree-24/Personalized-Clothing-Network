// Virtual Try-On Service using Hugging Face IDM-VTON model

const HF_API_URL = "https://api-inference.huggingface.co/models/yisol/IDM-VTON";

export interface VirtualTryOnRequest {
  personImage: string; // Base64 or URL
  garmentImage: string; // Base64 or URL
  category: "upper_body" | "lower_body" | "dresses";
}

export interface VirtualTryOnResponse {
  success: boolean;
  resultImage?: string; // Base64 encoded result
  error?: string;
}

/**
 * Perform virtual try-on using backend proxy
 * This avoids CORS issues and handles API key securely
 */
export async function performVirtualTryOn(
  request: VirtualTryOnRequest
): Promise<VirtualTryOnResponse> {
  try {
    // Use backend proxy to call Hugging Face API
    const response = await fetch("http://localhost:5000/api/virtual-tryon", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        person_image: request.personImage,
        garment_image: request.garmentImage,
        category: request.category,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || `API request failed: ${response.statusText}`);
    }

    const data = await response.json();

    return {
      success: true,
      resultImage: data.result_image,
    };
  } catch (error) {
    console.error("Virtual try-on error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error occurred",
    };
  }
}

/**
 * Convert image URL to base64
 */
export async function imageUrlToBase64(imageUrl: string): Promise<string> {
  try {
    const response = await fetch(imageUrl);
    const blob = await response.blob();
    return await blobToBase64(blob);
  } catch (error) {
    console.error("Error converting image to base64:", error);
    throw error;
  }
}

/**
 * Convert Blob to base64
 */
function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result as string);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

/**
 * Determine garment category from product title
 */
export function determineGarmentCategory(
  productTitle: string
): "upper_body" | "lower_body" | "dresses" {
  const title = productTitle.toLowerCase();

  if (title.includes("dress") || title.includes("gown")) {
    return "dresses";
  }

  if (
    title.includes("pant") ||
    title.includes("jean") ||
    title.includes("short") ||
    title.includes("skirt") ||
    title.includes("trouser")
  ) {
    return "lower_body";
  }

  // Default to upper body (shirts, tops, jackets, etc.)
  return "upper_body";
}

/**
 * Backend API endpoint for virtual try-on with product
 */
export async function virtualTryOnWithProduct(
  personImage: string,
  productId: string
): Promise<VirtualTryOnResponse> {
  try {
    // Get product details from backend
    const response = await fetch(`http://localhost:5000/api/products/${productId}`);
    
    if (!response.ok) {
      throw new Error("Failed to fetch product details");
    }

    const data = await response.json();
    const product = data.product;

    if (!product || !product.image_url) {
      throw new Error("Product image not found");
    }

    // Determine category
    const category = determineGarmentCategory(product.title);

    // Perform virtual try-on
    return await performVirtualTryOn({
      personImage,
      garmentImage: product.image_url,
      category,
    });
  } catch (error) {
    console.error("Virtual try-on with product error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error occurred",
    };
  }
}
