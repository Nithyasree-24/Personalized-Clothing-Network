// Simple Virtual Try-On using client-side image overlay
// This is a basic implementation that works without API calls

export interface SimpleOverlayResult {
  success: boolean;
  resultImage?: string;
  error?: string;
}

/**
 * Create a simple overlay of garment on person image
 * This is a basic implementation for demo purposes
 */
export async function simpleGarmentOverlay(
  personImageUrl: string,
  garmentImageUrl: string,
  category: "upper_body" | "lower_body" | "dresses"
): Promise<SimpleOverlayResult> {
  try {
    // Create canvas
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    
    if (!ctx) {
      throw new Error("Canvas not supported");
    }

    // Load images
    const personImg = await loadImage(personImageUrl);
    const garmentImg = await loadImage(garmentImageUrl);

    // Set canvas size to person image size
    canvas.width = personImg.width;
    canvas.height = personImg.height;

    // Draw person image
    ctx.drawImage(personImg, 0, 0);

    // Calculate garment position and size based on category
    const { x, y, width, height } = calculateGarmentPosition(
      personImg.width,
      personImg.height,
      category
    );

    // Set transparency for overlay
    ctx.globalAlpha = 0.8;

    // Draw garment with proper sizing
    ctx.drawImage(garmentImg, x, y, width, height);

    // Reset alpha
    ctx.globalAlpha = 1.0;

    // Convert to base64
    const resultImage = canvas.toDataURL("image/png");

    return {
      success: true,
      resultImage,
    };
  } catch (error) {
    console.error("Simple overlay error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}

/**
 * Load image from URL
 */
function loadImage(url: string): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = "anonymous";
    img.onload = () => resolve(img);
    img.onerror = reject;
    img.src = url;
  });
}

/**
 * Calculate garment position based on category
 */
function calculateGarmentPosition(
  canvasWidth: number,
  canvasHeight: number,
  category: "upper_body" | "lower_body" | "dresses"
): { x: number; y: number; width: number; height: number } {
  const centerX = canvasWidth / 2;

  switch (category) {
    case "upper_body":
      // Position for tops/shirts (upper 40% of image)
      return {
        x: centerX - canvasWidth * 0.25,
        y: canvasHeight * 0.15,
        width: canvasWidth * 0.5,
        height: canvasHeight * 0.35,
      };

    case "lower_body":
      // Position for pants/skirts (middle to lower)
      return {
        x: centerX - canvasWidth * 0.25,
        y: canvasHeight * 0.45,
        width: canvasWidth * 0.5,
        height: canvasHeight * 0.45,
      };

    case "dresses":
      // Position for dresses (upper to lower)
      return {
        x: centerX - canvasWidth * 0.3,
        y: canvasHeight * 0.15,
        width: canvasWidth * 0.6,
        height: canvasHeight * 0.7,
      };

    default:
      return {
        x: centerX - canvasWidth * 0.25,
        y: canvasHeight * 0.2,
        width: canvasWidth * 0.5,
        height: canvasHeight * 0.5,
      };
  }
}

/**
 * Create a side-by-side comparison
 */
export async function createComparison(
  personImageUrl: string,
  garmentImageUrl: string,
  category: "upper_body" | "lower_body" | "dresses"
): Promise<SimpleOverlayResult> {
  try {
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    
    if (!ctx) {
      throw new Error("Canvas not supported");
    }

    // Load images
    const personImg = await loadImage(personImageUrl);
    const garmentImg = await loadImage(garmentImageUrl);

    // Create overlay
    const overlayResult = await simpleGarmentOverlay(
      personImageUrl,
      garmentImageUrl,
      category
    );

    if (!overlayResult.success || !overlayResult.resultImage) {
      throw new Error("Failed to create overlay");
    }

    const overlayImg = await loadImage(overlayResult.resultImage);

    // Set canvas size for side-by-side
    canvas.width = personImg.width * 2 + 20; // 20px gap
    canvas.height = personImg.height;

    // Fill background
    ctx.fillStyle = "#f5f5f5";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw original on left
    ctx.drawImage(personImg, 0, 0);

    // Draw overlay on right
    ctx.drawImage(overlayImg, personImg.width + 20, 0);

    // Add labels
    ctx.fillStyle = "#000";
    ctx.font = "bold 24px Arial";
    ctx.fillText("Before", 20, 40);
    ctx.fillText("After", personImg.width + 40, 40);

    const resultImage = canvas.toDataURL("image/png");

    return {
      success: true,
      resultImage,
    };
  } catch (error) {
    console.error("Comparison error:", error);
    return {
      success: false,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
}
