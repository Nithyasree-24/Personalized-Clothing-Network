type AvatarConfig = {
  gender: "women" | "men" | "kids";
  skinTone: string;
  hairStyle: string;
  hairColor: string;
  eyeStyle: string;
  eyeColor: string;
  noseStyle: string;
  mouthStyle: string;
  faceShape: string;
  bodyType: string;
  outfit?: string;
};

type CustomAvatarProps = {
  config: AvatarConfig;
  size?: number;
  wornItems?: any[];
};

export default function CustomAvatar({ config, size = 300, wornItems = [] }: CustomAvatarProps) {
  const height = (size / 300) * 500;
  
  return (
    <svg width={size} height={height} viewBox="0 0 300 500" className="drop-shadow-2xl">
      <defs>
        <radialGradient id="skinGradient" cx="50%" cy="40%">
          <stop offset="0%" stopColor={config.skinTone} stopOpacity="1" />
          <stop offset="100%" stopColor={config.skinTone} stopOpacity="0.85" />
        </radialGradient>
        <linearGradient id="hairShine" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop offset="0%" stopColor="white" stopOpacity="0.4" />
          <stop offset="50%" stopColor={config.hairColor} stopOpacity="1" />
          <stop offset="100%" stopColor={config.hairColor} stopOpacity="0.8" />
        </linearGradient>
        <filter id="shadow">
          <feDropShadow dx="0" dy="2" stdDeviation="3" floodOpacity="0.3"/>
        </filter>
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
        <ellipse cx="132" cy="467" rx="15" ry="5" fill="white" opacity="0.2" />
        <ellipse cx="167" cy="467" rx="15" ry="5" fill="white" opacity="0.2" />
      </g>

      {/* Body/Torso */}
      <g>
        <rect x="105" y="240" width="90" height="120" rx="20" fill="#3A7BC8" stroke="#2A5A8E" strokeWidth="2" />
        <ellipse cx="150" cy="240" rx="45" ry="15" fill="#3A7BC8" />
        
        {/* Clothing details */}
        <line x1="150" y1="250" x2="150" y2="350" stroke="#2A5A8E" strokeWidth="2" />
        <circle cx="150" cy="270" r="4" fill="#1E4A6F" />
        <circle cx="150" cy="295" r="4" fill="#1E4A6F" />
        <circle cx="150" cy="320" r="4" fill="#1E4A6F" />
        
        {/* Collar */}
        <path d="M 130 245 L 140 255 L 150 245 L 160 255 L 170 245" stroke="#2A5A8E" strokeWidth="3" fill="none" strokeLinecap="round" />
      </g>

      {/* Arms */}
      <g>
        <ellipse cx="95" cy="280" rx="15" ry="50" fill="url(#skinGradient)" stroke={config.skinTone} strokeWidth="1" />
        <ellipse cx="205" cy="280" rx="15" ry="50" fill="url(#skinGradient)" stroke={config.skinTone} strokeWidth="1" />
        
        <rect x="80" y="250" width="30" height="60" rx="15" fill="#3A7BC8" />
        <rect x="190" y="250" width="30" height="60" rx="15" fill="#3A7BC8" />
        
        {/* Hands */}
        <ellipse cx="95" cy="330" rx="12" ry="15" fill={config.skinTone} />
        <ellipse cx="205" cy="330" rx="12" ry="15" fill={config.skinTone} />
      </g>

      {/* Neck */}
      <rect x="135" y="200" width="30" height="45" fill="url(#skinGradient)" rx="5" />
      <ellipse cx="150" cy="200" rx="20" ry="8" fill={config.skinTone} opacity="0.5" />

      {/* Head */}
      <ellipse 
        cx="150" 
        cy="140" 
        rx={config.faceShape === "round" ? "65" : config.faceShape === "long" ? "55" : "60"} 
        ry={config.faceShape === "round" ? "65" : config.faceShape === "long" ? "75" : "70"} 
        fill="url(#skinGradient)"
        stroke={config.skinTone}
        strokeWidth="2"
        filter="url(#shadow)"
      />

      {/* Ears */}
      <ellipse cx="90" cy="140" rx="10" ry="15" fill={config.skinTone} opacity="0.95" />
      <ellipse cx="210" cy="140" rx="10" ry="15" fill={config.skinTone} opacity="0.95" />
      <ellipse cx="92" cy="140" rx="5" ry="8" fill={config.skinTone} opacity="0.7" />
      <ellipse cx="208" cy="140" rx="5" ry="8" fill={config.skinTone} opacity="0.7" />

      {/* Hair - Detailed styles */}
      {config.hairStyle === "long" && (
        <>
          <ellipse cx="150" cy="95" rx="70" ry="45" fill="url(#hairShine)" />
          <path d="M 80 95 Q 75 180 85 230 L 95 230 Q 85 180 85 95 Z" fill={config.hairColor} stroke={config.hairColor} strokeWidth="1" />
          <path d="M 220 95 Q 225 180 215 230 L 205 230 Q 215 180 215 95 Z" fill={config.hairColor} stroke={config.hairColor} strokeWidth="1" />
          <ellipse cx="90" cy="170" rx="12" ry="55" fill={config.hairColor} opacity="0.95" />
          <ellipse cx="210" cy="170" rx="12" ry="55" fill={config.hairColor} opacity="0.95" />
          <path d="M 85 100 Q 80 150 85 200" stroke="white" strokeWidth="2" opacity="0.3" strokeLinecap="round" />
        </>
      )}

      {config.hairStyle === "short" && (
        <>
          <ellipse cx="150" cy="95" rx="68" ry="42" fill="url(#hairShine)" />
          <path d="M 82 110 Q 80 135 90 145" stroke={config.hairColor} strokeWidth="10" fill="none" strokeLinecap="round" />
          <path d="M 218 110 Q 220 135 210 145" stroke={config.hairColor} strokeWidth="10" fill="none" strokeLinecap="round" />
        </>
      )}

      {config.hairStyle === "curly" && (
        <>
          {[...Array(12)].map((_, i) => {
            const angle = (i / 12) * Math.PI * 2;
            const radius = 55;
            const x = 150 + Math.cos(angle) * radius;
            const y = 100 + Math.sin(angle) * radius * 0.7;
            const size = 20 + Math.random() * 8;
            return <circle key={i} cx={x} cy={y} r={size} fill={config.hairColor} opacity={0.9 + Math.random() * 0.1} />;
          })}
        </>
      )}

      {config.hairStyle === "wavy" && (
        <>
          <ellipse cx="150" cy="95" rx="70" ry="45" fill="url(#hairShine)" />
          <path d="M 80 115 Q 95 105 110 115 T 140 115 T 170 115 T 200 115 T 220 115" 
                stroke={config.hairColor} strokeWidth="18" fill="none" strokeLinecap="round" opacity="0.9" />
          <path d="M 85 135 Q 100 125 115 135 T 145 135 T 175 135 T 205 135" 
                stroke={config.hairColor} strokeWidth="15" fill="none" strokeLinecap="round" opacity="0.7" />
        </>
      )}

      {config.hairStyle === "ponytail" && (
        <>
          <ellipse cx="150" cy="95" rx="68" ry="40" fill="url(#hairShine)" />
          <ellipse cx="210" cy="140" rx="22" ry="60" fill={config.hairColor} />
          <ellipse cx="213" cy="140" rx="18" ry="55" fill="url(#hairShine)" />
          <circle cx="195" cy="110" r="18" fill={config.hairColor} />
          <path d="M 210 100 Q 215 120 210 140" stroke="white" strokeWidth="2" opacity="0.3" />
        </>
      )}

      {config.hairStyle === "bun" && (
        <>
          <ellipse cx="150" cy="95" rx="68" ry="38" fill="url(#hairShine)" />
          <circle cx="150" cy="70" r="28" fill={config.hairColor} />
          <circle cx="150" cy="70" r="24" fill="url(#hairShine)" />
          <ellipse cx="150" cy="75" rx="18" ry="6" fill={config.hairColor} opacity="0.6" />
        </>
      )}

      {config.hairStyle === "pigtails" && (
        <>
          <ellipse cx="150" cy="95" rx="65" ry="38" fill="url(#hairShine)" />
          <ellipse cx="95" cy="140" rx="16" ry="45" fill={config.hairColor} />
          <ellipse cx="205" cy="140" rx="16" ry="45" fill={config.hairColor} />
          <circle cx="100" cy="110" r="18" fill={config.hairColor} />
          <circle cx="200" cy="110" r="18" fill={config.hairColor} />
        </>
      )}

      {config.hairStyle === "bob" && (
        <>
          <ellipse cx="150" cy="95" rx="70" ry="42" fill="url(#hairShine)" />
          <rect x="80" y="110" width="140" height="60" fill={config.hairColor} rx="30" />
          <ellipse cx="150" cy="140" rx="70" ry="30" fill="url(#hairShine)" />
        </>
      )}

      {/* Eyebrows */}
      <path d="M 115 125 Q 130 120 145 125" stroke={config.hairColor} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.85" />
      <path d="M 155 125 Q 170 120 185 125" stroke={config.hairColor} strokeWidth="4" fill="none" strokeLinecap="round" opacity="0.85" />

      {/* Eyes */}
      <g>
        <ellipse cx="130" cy="145" rx="14" ry={config.eyeStyle === "wide" ? "16" : "12"} fill="white" />
        <ellipse cx="170" cy="145" rx="14" ry={config.eyeStyle === "wide" ? "16" : "12"} fill="white" />
        
        <circle cx="130" cy="145" r="8" fill={config.eyeColor} />
        <circle cx="170" cy="145" r="8" fill={config.eyeColor} />
        
        <circle cx="130" cy="145" r="4" fill="black" />
        <circle cx="170" cy="145" r="4" fill="black" />
        
        <circle cx="132" cy="143" r="2.5" fill="white" opacity="0.9" />
        <circle cx="172" cy="143" r="2.5" fill="white" opacity="0.9" />
        
        {/* Eyelashes */}
        <path d="M 117 140 L 114 137" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 120 138 L 118 134" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 143 140 L 146 137" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 140 138 L 142 134" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        
        <path d="M 157 140 L 154 137" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 160 138 L 158 134" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 183 140 L 186 137" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
        <path d="M 180 138 L 182 134" stroke="black" strokeWidth="1.5" strokeLinecap="round" />
      </g>

      {/* Nose */}
      <ellipse cx="150" cy="160" rx="8" ry="10" fill={config.skinTone} opacity="0.5" />
      <ellipse cx="146" cy="167" rx="3" ry="4" fill={config.skinTone} opacity="0.7" />
      <ellipse cx="154" cy="167" rx="3" ry="4" fill={config.skinTone} opacity="0.7" />
      <path d="M 150 155 L 150 167" stroke={config.skinTone} strokeWidth="2" opacity="0.4" />

      {/* Mouth */}
      {config.mouthStyle === "smile" && (
        <>
          <path d="M 130 180 Q 150 192 170 180" stroke="#D4756E" strokeWidth="4" fill="none" strokeLinecap="round" />
          <path d="M 135 183 Q 150 190 165 183" stroke="#FF9999" strokeWidth="2" fill="none" strokeLinecap="round" />
        </>
      )}
      {config.mouthStyle === "grin" && (
        <>
          <path d="M 130 180 Q 150 198 170 180" stroke="#D4756E" strokeWidth="4" fill="none" strokeLinecap="round" />
          <ellipse cx="150" cy="190" rx="20" ry="8" fill="white" />
        </>
      )}
      {config.mouthStyle === "neutral" && (
        <line x1="135" y1="180" x2="165" y2="180" stroke="#D4756E" strokeWidth="3" strokeLinecap="round" />
      )}

      {/* Blush */}
      <ellipse cx="115" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.5" />
      <ellipse cx="185" cy="160" rx="15" ry="10" fill="#FFB6C1" opacity="0.5" />

      {/* Worn items badges */}
      {wornItems.length > 0 && (
        <g>
          {wornItems.slice(0, 3).map((item, i) => (
            <g key={i} transform={`translate(${220 + i * 25}, ${120 + i * 25})`}>
              <circle cx="0" cy="0" r="12" fill="white" stroke="#EC4899" strokeWidth="2" />
              <text x="0" y="5" textAnchor="middle" fontSize="14">{item.emoji}</text>
            </g>
          ))}
        </g>
      )}
    </svg>
  );
}
