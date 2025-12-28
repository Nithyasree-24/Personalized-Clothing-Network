export type AgeGroup = "adult" | "kid";
export type Gender = "male" | "female" | "other";

export type BaseAvatar = {
  id: string;
  ageGroup: AgeGroup;
  gender: Gender;
  faceStyle: string;
  skinTone: string;
  hairStyle: string;
  hairColor: string;
  bodyType: string;
  eyeStyle: string;
  eyeColor: string;
};

export type AppliedSticker = {
  sticker_id: string;
  product_id: string;
  category: "top" | "bottom" | "outerwear" | "shoes" | "accessory";
  position: { x: number; y: number };
  scale: number;
  zIndex: number;
};

export type SavedOutfit = {
  id: string;
  name: string;
  avatar: BaseAvatar;
  stickers: AppliedSticker[];
  createdAt: string;
};

export type ProductSticker = {
  sticker_id: string;
  product_id: string;
  product_title: string;
  product_price: number;
  product_imageUrl: string;
  sticker_image: string; // URL to transparent PNG/SVG
  category: "top" | "bottom" | "outerwear" | "shoes" | "accessory";
  anchor_point: "chest" | "hips" | "feet" | "head" | "hand";
  default_position: { x: number; y: number };
  default_scale: number;
};
