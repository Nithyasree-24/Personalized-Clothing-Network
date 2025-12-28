"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

type SidebarProps = {
  selected?: string | null;
  onSelect?: (category: string | null) => void;
};

const items = [
  { 
    key: "Women", 
    icon: "👩",
    categories: ["All Women", "Western Wear", "Dresses", "Ethnic Wear", "Tops and Co-ord Sets", "Women's Bottomwear"],
    link: null
  },
  { 
    key: "Men", 
    icon: "👨",
    categories: ["All Men", "shirts", "T-shirts", "Bottom Wear", "Hoodies"],
    link: null
  },
];

export default function Sidebar({ selected = null, onSelect }: SidebarProps) {
  const router = useRouter();
  const [expandedSection, setExpandedSection] = useState<string | null>(null);
  const [isOpen, setIsOpen] = useState(false);

  const handleMainClick = (key: string, link?: string | null) => {
    // If there's a link, navigate to that page
    if (link) {
      router.push(link);
      setIsOpen(false);
      return;
    }

    // Otherwise, expand/collapse the section
    if (expandedSection === key) {
      setExpandedSection(null);
      onSelect?.(null);
    } else {
      setExpandedSection(key);
      onSelect?.(key);
    }
  };

  return (
    <>
      {/* Toggle Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed left-4 top-24 z-40 bg-gradient-to-br from-pink-500 to-pink-700 text-white rounded-full p-3 shadow-lg hover:shadow-xl transition-all hover:from-pink-600 hover:to-pink-800"
        title="Explore Categories"
      >
        <svg className="w-6 h-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16"/>
        </svg>
      </button>

      {/* Sidebar Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/30 z-40"
          onClick={() => setIsOpen(false)}
        />
      )}

      {/* Sidebar Panel */}
      <aside className={`fixed left-0 top-0 h-full w-80 bg-gradient-to-b from-pink-50 to-white shadow-2xl z-50 transform transition-transform duration-300 ${isOpen ? 'translate-x-0' : '-translate-x-full'}`}>
        <nav className="h-full overflow-y-auto p-6">
        <div className="flex items-center justify-between mb-6">
          <h3 className="text-2xl font-bold bg-gradient-to-r from-pink-600 to-pink-800 bg-clip-text text-transparent">Categories</h3>
          <button
            onClick={() => setIsOpen(false)}
            className="text-pink-400 hover:text-pink-600 text-2xl"
          >
            ✕
          </button>
        </div>

        {/* Categories Section */}
        <div>
          <h4 className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3 px-3">Shop Categories</h4>
          <ul className="space-y-2">
            {items.map((it) => {
            const isExpanded = expandedSection === it.key;
            const active = selected === it.key;
            return (
              <li key={it.key}>
                <div
                  onClick={() => handleMainClick(it.key, it.link)}
                  className={`flex cursor-pointer items-center justify-between gap-3 rounded-lg px-3 py-2 transition-colors text-black ${
                    active ? "bg-gradient-to-r from-pink-100 to-pink-200 font-medium text-pink-700" : "hover:bg-pink-50"
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-sm">{it.icon}</span>
                    <span className="text-sm">{it.key}</span>
                    {it.link && <span className="text-xs text-pink-500">→</span>}
                  </div>
                  {!it.link && <span className={`text-sm font-bold transition-transform ${isExpanded ? 'rotate-45' : ''} text-pink-500`}>+</span>}
                </div>
                
                {isExpanded && (
                  <ul className="mt-2 ml-6 space-y-1 animate-slideDown">
                    {it.categories.map((cat) => (
                      <li
                        key={cat}
                        onClick={() => {
                          console.log("Category selected:", cat);
                          onSelect?.(cat);
                        }}
                        className={`cursor-pointer rounded-lg px-3 py-1.5 text-xs transition-colors ${
                          selected === cat 
                            ? "bg-gradient-to-r from-pink-500 to-pink-600 text-white font-medium" 
                            : "text-gray-600 hover:bg-pink-100 hover:text-pink-700"
                        }`}
                      >
                        {cat}
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            );
          })}
          </ul>
        </div>
      </nav>
    </aside>
    </>
  );
}
