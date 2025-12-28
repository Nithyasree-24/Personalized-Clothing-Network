"use client";

import { useRef, useEffect } from "react";
import { BaseAvatar, AppliedSticker } from "../../types/avatar";

type AvatarCanvasProps = {
  avatar: BaseAvatar;
  appliedStickers: AppliedSticker[];
  size?: number;
};

export default function AvatarCanvas({ avatar, appliedStickers, size = 300 }: AvatarCanvasProps) {
  const canvasRef = useRef<HTMLDivElement>(null);
  const height = (size / 300) * 500;

  return (
    <div ref={canvasRef} className="relative inline-block">
      <svg width={size} height={height} viewBox="0 0 300 500" className="drop-shadow-2xl">
        <defs>
          <radialGradient id={`skinGradient-${avatar.id}`} cx="50%" cy="40%">
            <stop offset="0%" stopColor={avatar.skinTone} stopOpacity="1" />
            <stop offset="100%" stopColor={avatar.skinTone} stopOpacity="0.85" />
          </radialGradient>
          <linearGradient id={`hairShine-${avatar.id}`} x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stopColor="white" stopOpacity="0.4" />
            <stop offset="50%" stopColor={avatar.hairColor} stopOpacity="1" />
            <stop offset="100%" stopColor={avatar.hairColor} stopOpacity="0.8" />
          </linearGradient>
        </defs>

        {/* Legs */}
        <g>
          <rect x="120" y="350" width="25" height="120" rx="12" fill="#2C5F8D" stroke="#1E4A6F" strokeWidth="2" />
          <rect x="155" y="350" width="25" height="120" rx="12" fill="#2C5F8D" stroke="#1E4A6F" strokeWidth="2" />
          
          {/* Shoes */}
          <ellipse cx="132" cy="475" rx="18" ry="12" fill="#4A4A4A" />
          <ellipse cx="167" cy="475" rx="18" ry="12" fill="#4A4A4A" />
          <rect x="114" y="465" width="36" height="15" rx="8" fill="#5A5A5A" />
          <rect x="149" y="465" width="36" height="15" rx="8" fill="#5A5A5A" />
        </g>

        {/* Body/Torso */}
        <g>
          <rect x="105" y="240" width="90" height="120" rx="20" fill="#3A7BC8" stroke="#2A5A8E" strokeWidth="2" />
          <ellipse cx="150" cy="240" rx="45" ry="15" fill="#3A7BC8" />
          <line x1="150" y1="250" x2="150" y2="350" stroke="#2A5A8E" strokeWidth="2" />
          <circle cx="150" cy="270" r="4" fill="#1E4A6F" />
          <circle cx="150" cy="295" r="4" fill="#1E4A6F" />
          <circle cx="150" cy="320" r="4" fill="#1E4A6F" />
        </g>

        {/* Arms */}
        <g>
          <ellipse cx="95" cy="280" rx="15" ry="50" fill={`url(#skinGradient-${avatar.id})`} />
          <ellipse cx="205" cy="280" rx="15" ry="50" fill={`url(#skinGradient-${avatar.id})`} />
          <rect x="80" y="250" width="30" height="60" rx="15" fill="#3A7BC8" />
          <rect x="190" y="250" width="30" height="60" rx="15" fill="#3A7BC8" />
          <ellipse cx="95" cy="330" rx="12" ry="15" fill={avatar.skinTone} />
          <ellipse cx="205" cy="330" rx="12" ry="15" fill={avatar.skinTone} />
        </g>

        {/* Neck */}
        <rect x="135" y="200" width="30" height="45" fill={`url(#skinGradient-${avatar.id})`} rx="5" />

        {/* Head */}
        <ellipse 
          cx="150" 
          cy="140" 
          rx={avatar.faceStyle === "round" ? "65" : avatar.faceStyle === "long" ? "55" : "60"} 
          ry={avatar.faceStyle === "round" ? "65" : avatar.faceStyle === "long" ? "75" : "70"} 
          fill={`url(#skinGradient-${avatar.id})`}
          stroke={avatar.skinTone}
          strokeWidth="2"
        />

        {/* Ears */}
        <ellipse cx="90" cy="140" rx="10" ry="15" fill={avatar.skinTone} opacity="0.95" />
        <ellipse cx="210" cy="140" rx="10" ry="15" fill={avatar.skinTone} opacity="0.95" />

        {/* Hair */}
        {avatar.hairStyle === "long" && (
          <>
            <ellipse cx="150" cy="95" rx="70" ry="45" fill={`url(#hairShine-${avatar.id})`} />
            <path d="M 80 95 Q 75 180 85 230 L 95 230 Q 85 180 85 95 Z" fill={avatar.hairColor} />
            <path d="M 220 95 Q 225 180 215 230 L 205 230 Q 215 180 215 95 Z" fill={avatar.hairColor} />
          </>
        )}
        {avatar.hairStyle === "short" && (
          <ellipse cx="150" cy="95" rx="68" ry="42" fill={`url(#hairShine-${avatar.id})`} />
        )}
        {avatar.hairStyle === "curly" && (
          <>
            {[...Array(12)].map((_, i) => {
              const angle = (i / 12) * Math.PI * 2;
              const radius = 55;
              const x = 150 + Math.cos(angle) * radius;
              const y = 100 + Math.sin(angle) * radius * 0.7;
              const circleSize = 20 + Math.random() * 8;
              return <circle key={i} cx={x} cy={y} r={circleSize} fill={avatar.hairColor} opacity={0.9} />;
            })}
          </>
        )}
        {avatar.hairStyle === "ponytail" && (
          <>
            <ellipse cx="150" cy="95" rx="68" ry="40" fill={`url(#hairShine-${avatar.id})`} />
            <ellipse cx="210" cy="140" rx="22" ry="60" fill={avatar.hairColor} />
            <circle cx="195" cy="110" r="18" fill={avatar.hairColor} />
          </>
        )}
        {avatar.hairStyle === "bun" && (
          <>
            <ellipse cx="150" cy="95" rx="68" ry="38" fill={`url(#hairShine-${avatar.id})`} />
            <circle cx="150" cy="70" r="28" fill={avatar.hairColor} />
          </>
        )}

        {/* Eyes */}
        <g>
          <ellipse cx="130" cy="145" rx="14" ry="12" fill="white" />
          <ellipse cx="170" cy="145" rx="14" ry="12" fill="white" />
          <circle cx="130" cy="145" r="8" fill={avatar.eyeColor} />
          <circle cx="170" cy="145" r="8" fill={avatar.eyeColor} />
          <circle cx="130" cy="145" r="4" fill="black" />
          <circle cx="170" cy="145" r="4" fill="black" />
          <circle cx="132" cy="143" r="2.5" fill="white" opacity="0.9" />
          <circle cx="172" cy="143" r="2.5" fill="white" opacity="0.9" />
        </g>

        {/* Eyebrows */}
        <path d="M 115 125 Q 130 120 145 125" stroke={avatar.hairColor} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.85" />
        <path d="M 155 125 Q 170 120 185 125" stroke={avatar.hairColor} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.85" />

        {/* Nose */}
        <ellipse cx="150" cy="160" rx="8" ry="10" fill={avatar.skinTone} opacity="0.5" />

        {/* Mouth */}
        <path d="M 130 180 Q 150 192 170 180" stroke="#D4756E" strokeWidth="4" fill="none" strokeLinecap="round" />

        {/* Blush */}
        <ellipse cx="115" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.5" />
        <ellipse cx="185" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.5" />
      </svg>

      {/* Applied Stickers Layer */}
      {appliedStickers.length > 0 && (
        <div className="absolute top-0 left-0 w-full h-full pointer-events-none">
          {appliedStickers
            .sort((a, b) => a.zIndex - b.zIndex)
            .map((sticker) => (
              <div
                key={sticker.sticker_id}
                className="absolute"
                style={{
                  left: `${sticker.position.x}%`,
                  top: `${sticker.position.y}%`,
                  transform: `translate(-50%, -50%) scale(${sticker.scale})`,
                  zIndex: sticker.zIndex,
                }}
              >
                <span className="text-4xl">{sticker.sticker_id}</span>
              </div>
            ))}
        </div>
      )}
    </div>
  );
}
