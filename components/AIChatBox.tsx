"use client";

import { useState, useEffect, useRef } from "react";
import { useCart } from "../context/CartContext";

interface Message {
  text: string;
  isUser: boolean;
  timestamp: string;
  products?: Product[];
  showAllProducts?: boolean; // New field to track if all products should be shown
  type?: string; // Add type field for special messages
  options?: string[]; // Add options for interactive buttons
  flowState?: any; // Add flow state for multi-step processes
}

interface Product {
  product_id: string;
  product_name: string;
  price: number;
  product_image: string;
  color: string;
  gender: string;
  product_category: string;
  stock: number;
  product_description?: string;
}

// Custom Calendar Component
interface CustomCalendarProps {
  onDateSelect: (year: number, month: number, day: number) => void;
  selectedDate?: string;
}

const CustomCalendar: React.FC<CustomCalendarProps> = ({ onDateSelect, selectedDate }) => {
  const [currentStep, setCurrentStep] = useState<'year' | 'month' | 'day'>('year');
  const [selectedYear, setSelectedYear] = useState<number>(new Date().getFullYear());
  const [selectedMonth, setSelectedMonth] = useState<number>(new Date().getMonth());
  
  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 5 }, (_, i) => currentYear + i);
  
  const months = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
  ];
  
  const getDaysInMonth = (year: number, month: number) => {
    return new Date(year, month + 1, 0).getDate();
  };
  
  const getFirstDayOfMonth = (year: number, month: number) => {
    return new Date(year, month, 1).getDay();
  };
  
  const isMonthInPast = (year: number, month: number) => {
    const today = new Date();
    const currentYear = today.getFullYear();
    const currentMonth = today.getMonth();
    
    if (year < currentYear) return true;
    if (year === currentYear && month < currentMonth) return true;
    return false;
  };
  
  const handleYearSelect = (year: number) => {
    setSelectedYear(year);
    setCurrentStep('month');
  };
  
  const handleMonthSelect = (monthIndex: number) => {
    setSelectedMonth(monthIndex);
    setCurrentStep('day');
  };
  
  const handleDaySelect = (day: number) => {
    onDateSelect(selectedYear, selectedMonth, day);
  };
  
  const goBack = () => {
    if (currentStep === 'month') {
      setCurrentStep('year');
    } else if (currentStep === 'day') {
      setCurrentStep('month');
    }
  };
  
  return (
    <div className="w-full max-w-md mx-auto">
      {/* Header with back button */}
      <div className="flex items-center justify-between mb-4">
        {currentStep !== 'year' && (
          <button
            onClick={goBack}
            className="flex items-center gap-2 text-purple-600 hover:text-purple-800 font-medium"
          >
            <span>←</span>
            <span>Back</span>
          </button>
        )}
        <div className="text-lg font-bold text-gray-800">
          {currentStep === 'year' && 'Select Year'}
          {currentStep === 'month' && `Select Month - ${selectedYear}`}
          {currentStep === 'day' && `Select Day - ${months[selectedMonth]} ${selectedYear}`}
        </div>
        <div></div> {/* Spacer for centering */}
      </div>
      
      {/* Year Selection */}
      {currentStep === 'year' && (
        <div className="grid grid-cols-2 gap-3">
          {years.map((year) => (
            <button
              key={year}
              onClick={() => handleYearSelect(year)}
              className="bg-white border-2 border-purple-200 hover:border-purple-400 hover:bg-purple-50 rounded-xl p-4 font-semibold text-gray-800 transition-all"
            >
              {year}
            </button>
          ))}
        </div>
      )}
      
      {/* Month Selection */}
      {currentStep === 'month' && (
        <div className="grid grid-cols-3 gap-2">
          {months.map((month, index) => {
            const isPastMonth = isMonthInPast(selectedYear, index);
            
            if (isPastMonth) return null; // Don't render past months
            
            return (
              <button
                key={month}
                onClick={() => handleMonthSelect(index)}
                className="bg-white border-2 border-purple-200 hover:border-purple-400 hover:bg-purple-50 rounded-lg p-3 font-medium text-gray-800 transition-all text-sm"
              >
                {month.substring(0, 3)}
              </button>
            );
          })}
        </div>
      )}
      
      {/* Day Selection */}
      {currentStep === 'day' && (
        <div>
          {/* Days of week header */}
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
              <div key={day} className="text-center text-xs font-medium text-gray-500 p-2">
                {day}
              </div>
            ))}
          </div>
          
          {/* Calendar grid */}
          <div className="grid grid-cols-7 gap-1">
            {/* Empty cells for days before month starts */}
            {Array.from({ length: getFirstDayOfMonth(selectedYear, selectedMonth) }).map((_, index) => (
              <div key={`empty-${index}`} className="p-2"></div>
            ))}
            
            {/* Days of the month */}
            {Array.from({ length: getDaysInMonth(selectedYear, selectedMonth) }).map((_, index) => {
              const day = index + 1;
              const today = new Date();
              const isToday = selectedYear === today.getFullYear() && 
                            selectedMonth === today.getMonth() && 
                            day === today.getDate();
              const isPast = new Date(selectedYear, selectedMonth, day) < new Date(today.getFullYear(), today.getMonth(), today.getDate());
              
              return (
                <button
                  key={day}
                  onClick={() => !isPast && handleDaySelect(day)}
                  disabled={isPast}
                  className={`
                    p-2 text-sm font-medium rounded-lg transition-all
                    ${isPast 
                      ? 'text-gray-300 cursor-not-allowed' 
                      : 'text-gray-800 hover:bg-purple-100 hover:border-purple-300'
                    }
                    ${isToday ? 'bg-purple-200 border-2 border-purple-400' : 'bg-white border border-gray-200'}
                  `}
                >
                  {day}
                </button>
              );
            })}
          </div>
          
          <div className="text-xs text-gray-500 mt-3 text-center">
            Past dates are disabled. Select a future date for your event.
          </div>
        </div>
      )}
    </div>
  );
};

export default function AIChatBox() {
  const { cart, wishlist } = useCart();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { 
      text: "Hi! I'm your fashion assistant. What are you looking for today?\n\nChoose an option:\n• Browse Products - Search our collection\n• View Cart - Check your shopping cart\n• My Wishlist - See saved items\n• My Orders - View order history\n\nChoose query option:\n• Red dresses under ₹2000\n• Blue shirts for men\n• Black tops for women\n• White ethnic wear", 
      isUser: false,
      timestamp: new Date().toISOString(),
      options: ["Browse Products", "View Cart", "My Wishlist", "My Orders", "Red dresses under ₹2000", "Blue shirts for men", "Black tops for women", "White ethnic wear"]
    },
  ]);
  const [inputText, setInputText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`);
  
  // Flow state management
  const [currentFlow, setCurrentFlow] = useState<'none' | 'face_tone' | 'body_fit' | 'calendar'>('none');
  const [flowData, setFlowData] = useState<any>({});

  // Menu state management
  const [showDropdown, setShowDropdown] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showFeatures, setShowFeatures] = useState(false);
  const [chatHistory, setChatHistory] = useState<any[]>([]);

  // Calendar state management
  const [showCalendar, setShowCalendar] = useState(false);
  const [calendarStep, setCalendarStep] = useState<'gender' | 'date' | 'event' | 'complete'>('gender');
  const [calendarData, setCalendarData] = useState<{
    gender?: string;
    date?: string;
    event?: string;
    selectedYear?: number;
    selectedMonth?: number;
    selectedDay?: number;
  }>({});
  const [userEvents, setUserEvents] = useState<any[]>([]);
  const [hasUpcomingEvents, setHasUpcomingEvents] = useState(false);
  const [showCustomEventInput, setShowCustomEventInput] = useState(false);

  // Function to reset chat to initial state with options
  const resetChatToInitialState = () => {
    setMessages([
      { 
        text: "Hi! I'm your fashion assistant. What are you looking for today?\n\nChoose an option:\n• Browse Products - Search our collection\n• View Cart - Check your shopping cart\n• My Wishlist - See saved items\n• My Orders - View order history\n\nChoose query option:\n• Red dresses under ₹2000\n• Blue shirts for men\n• Black tops for women\n• White ethnic wear", 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: ["Browse Products", "View Cart", "My Wishlist", "My Orders", "Red dresses under ₹2000", "Blue shirts for men", "Black tops for women", "White ethnic wear"]
      },
    ]);
    setCurrentFlow('none');
    setFlowData({});
  };

  // Chat history management
  const saveChatToHistory = () => {
    const userId = localStorage.getItem('user_id') || 'guest';
    const historyKey = `fashionpulse_history_${userId}`;
    
    const chatSession = {
      id: `${sessionId}_${Date.now()}`, // Make ID unique with timestamp
      messages: messages,
      timestamp: new Date().toISOString(),
      title: `Chat ${new Date().toLocaleDateString()}`
    };
    
    const existingHistory = JSON.parse(localStorage.getItem(historyKey) || '[]');
    const updatedHistory = [chatSession, ...existingHistory.slice(0, 9)]; // Keep last 10 chats
    
    localStorage.setItem(historyKey, JSON.stringify(updatedHistory));
    setChatHistory(updatedHistory);
  };

  const loadChatHistory = () => {
    const userId = localStorage.getItem('user_id') || 'guest';
    const historyKey = `fashionpulse_history_${userId}`;
    const history = JSON.parse(localStorage.getItem(historyKey) || '[]');
    setChatHistory(history);
  };

  const loadHistoryChat = (historyItem: any) => {
    setMessages(historyItem.messages);
    setShowHistory(false);
    setShowDropdown(false);
  };

  const handleDropdownAction = (action: string) => {
    if (action === 'history') {
      loadChatHistory();
      setShowHistory(true);
      setShowFeatures(false);
    } else if (action === 'features') {
      setShowFeatures(true);
      setShowHistory(false);
    }
    setShowDropdown(false);
  };

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Load chat state from localStorage on component mount
  useEffect(() => {
    const userId = localStorage.getItem('user_id') || 'guest';
    
    // Load user events and check for upcoming events
    loadUserEvents();
    checkUpcomingEvents();
    
    // Check if returning from product page
    const returnState = sessionStorage.getItem('fashionpulse_chat_return');
    if (returnState) {
      try {
        const { isOpen: wasOpen, messages: returnMessages, fromChat } = JSON.parse(returnState);
        if (fromChat && wasOpen && returnMessages) {
          setIsOpen(true);
          setMessages(returnMessages);
          sessionStorage.removeItem('fashionpulse_chat_return');
          console.log('Chat restored from product page navigation');
          return;
        }
      } catch (error) {
        console.error('Error restoring chat from return state:', error);
      }
    }
    
    // Always start with fresh chat - don't restore previous conversations
    // Previous conversations are stored in history and accessible via menu
    console.log('Starting fresh chat session for user:', userId);
  }, []);

  // Calendar and Event Management Functions
  const loadUserEvents = () => {
    const userId = localStorage.getItem('user_id') || 'guest';
    const eventsKey = `fashionpulse_events_${userId}`;
    const events = JSON.parse(localStorage.getItem(eventsKey) || '[]');
    setUserEvents(events);
  };

  const saveUserEvent = (eventData: any) => {
    const userId = localStorage.getItem('user_id') || 'guest';
    const eventsKey = `fashionpulse_events_${userId}`;
    
    const newEvent = {
      id: `event_${Date.now()}_${Math.random().toString(36).substring(2, 11)}`,
      ...eventData,
      createdAt: new Date().toISOString(),
      userId: userId
    };
    
    const existingEvents = JSON.parse(localStorage.getItem(eventsKey) || '[]');
    const updatedEvents = [newEvent, ...existingEvents];
    
    localStorage.setItem(eventsKey, JSON.stringify(updatedEvents));
    setUserEvents(updatedEvents);
    
    return newEvent;
  };

  const checkUpcomingEvents = () => {
    const userId = localStorage.getItem('user_id') || 'guest';
    const eventsKey = `fashionpulse_events_${userId}`;
    const events = JSON.parse(localStorage.getItem(eventsKey) || '[]');
    
    const today = new Date();
    const threeDaysFromNow = new Date();
    threeDaysFromNow.setDate(today.getDate() + 3);
    
    const upcomingEvents = events.filter((event: any) => {
      const eventDate = new Date(event.date);
      return eventDate >= today && eventDate <= threeDaysFromNow;
    });
    
    setHasUpcomingEvents(upcomingEvents.length > 0);
    
    // Show reminder if there are upcoming events and chat is opened
    if (upcomingEvents.length > 0 && isOpen) {
      showEventReminders(upcomingEvents);
    }
  };

  const showEventReminders = (upcomingEvents: any[]) => {
    upcomingEvents.forEach((event, index) => {
      setTimeout(() => {
        const eventDate = new Date(event.date).toLocaleDateString();
        const daysUntil = Math.ceil((new Date(event.date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24));
        
        let reminderText = `🔔 **Event Reminder**\n\n`;
        reminderText += `Your event "${event.event}" on ${eventDate} is `;
        reminderText += daysUntil === 0 ? 'today!' : daysUntil === 1 ? 'tomorrow!' : `in ${daysUntil} days!`;
        reminderText += `\n\nHere are the best outfit suggestions for you:`;
        
        setMessages((prev) => [...prev, {
          text: reminderText,
          isUser: false,
          timestamp: new Date().toISOString(),
          type: 'event_reminder'
        }]);
        
        // Get outfit suggestions for this event
        getEventOutfitSuggestions(event);
      }, index * 1000); // Stagger reminders by 1 second
    });
  };

  const getEventOutfitSuggestions = async (event: any) => {
    try {
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: JSON.stringify({
            type: 'eventOutfitSuggestion',
            gender: event.gender,
            eventType: event.event,
            eventDate: event.date
          })
        })
      });
      
      const data = await response.json();
      
      if (data.products && data.products.length > 0) {
        setMessages((prev) => [...prev, {
          text: data.response || `Perfect outfits for your ${event.event}:`,
          isUser: false,
          timestamp: new Date().toISOString(),
          products: data.products,
          type: 'event_suggestions'
        }]);
      }
    } catch (error) {
      console.error('Error getting event outfit suggestions:', error);
    }
  };

  const handleCalendarClick = () => {
    setShowCalendar(true);
    setCalendarStep('gender');
    setCalendarData({});
  };

  const handleCalendarStep = async (selection: string) => {
    if (calendarStep === 'gender') {
      setCalendarData({ ...calendarData, gender: selection });
      setCalendarStep('date');
    } else if (calendarStep === 'date') {
      setCalendarData({ ...calendarData, date: selection });
      setCalendarStep('event');
    } else if (calendarStep === 'event') {
      if (selection === 'Others') {
        setShowCustomEventInput(true);
        return;
      }
      
      const eventData = {
        ...calendarData,
        event: selection,
        date: calendarData.date
      };
      
      // Save the event
      const savedEvent = saveUserEvent(eventData);
      
      // Show confirmation message
      setMessages((prev) => [...prev, {
        text: `✅ **Event Saved Successfully!**\n\n📅 **${savedEvent.event}** on ${new Date(savedEvent.date).toLocaleDateString()}\n👤 Gender: ${savedEvent.gender}\n\n🔔 I'll remind you closer to the date with perfect outfit suggestions!`,
        isUser: false,
        timestamp: new Date().toISOString(),
        type: 'event_confirmation'
      }]);
      
      // Close calendar
      setShowCalendar(false);
      setCalendarStep('gender');
      setCalendarData({});
      setShowCustomEventInput(false);
      
      // Check for upcoming events and show suggestions if event is soon
      checkUpcomingEvents();
      
      // If event is within 7 days, show immediate outfit suggestions
      const eventDate = new Date(savedEvent.date);
      const today = new Date();
      const daysUntil = Math.ceil((eventDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
      
      if (daysUntil <= 7 && daysUntil >= 0) {
        setTimeout(() => {
          getEventOutfitSuggestions(savedEvent);
        }, 1000);
      }
    }
  };

  const handleCustomEventSave = async (customEvent: string) => {
    if (!customEvent.trim()) return;
    
    const eventData = {
      ...calendarData,
      event: customEvent.trim(),
      date: calendarData.date
    };
    
    // Save the event
    const savedEvent = saveUserEvent(eventData);
    
    // Show confirmation message
    setMessages((prev) => [...prev, {
      text: `✅ **Custom Event Saved Successfully!**\n\n📅 **${savedEvent.event}** on ${new Date(savedEvent.date).toLocaleDateString()}\n👤 Gender: ${savedEvent.gender}\n\n🔔 I'll remind you closer to the date with perfect outfit suggestions!`,
      isUser: false,
      timestamp: new Date().toISOString(),
      type: 'event_confirmation'
    }]);
    
    // Close calendar
    setShowCalendar(false);
    setCalendarStep('gender');
    setCalendarData({});
    setShowCustomEventInput(false);
    
    // Check for upcoming events
    checkUpcomingEvents();
    
    // If event is within 7 days, show immediate outfit suggestions
    const eventDate = new Date(savedEvent.date);
    const today = new Date();
    const daysUntil = Math.ceil((eventDate.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));
    
    if (daysUntil <= 7 && daysUntil >= 0) {
      setTimeout(() => {
        getEventOutfitSuggestions(savedEvent);
      }, 1000);
    }
  };

  const handleDateSelection = (year: number, month: number, day: number) => {
    const selectedDate = new Date(year, month, day);
    const dateString = selectedDate.toISOString().split('T')[0];
    
    setCalendarData({ 
      ...calendarData, 
      date: dateString,
      selectedYear: year,
      selectedMonth: month,
      selectedDay: day
    });
    setCalendarStep('event');
  };

  // Also check for chat restoration on every render (in case useEffect misses it)
  useEffect(() => {
    const checkChatRestore = () => {
      const returnState = sessionStorage.getItem('fashionpulse_chat_return');
      if (returnState && !isOpen) {
        try {
          const { isOpen: wasOpen, messages: returnMessages, fromChat } = JSON.parse(returnState);
          if (fromChat && wasOpen && returnMessages) {
            setIsOpen(true);
            setMessages(returnMessages);
            sessionStorage.removeItem('fashionpulse_chat_return');
            console.log('Chat restored via secondary check');
          }
        } catch (error) {
          console.error('Error in secondary chat restore:', error);
        }
      }
    };

    // Check immediately and also set up interval
    checkChatRestore();
    const interval = setInterval(checkChatRestore, 500);
    
    return () => clearInterval(interval);
  }, [isOpen]);

  // Save chat to history only (don't restore previous chats in main chat)
  useEffect(() => {
    // Auto-save to history when there are meaningful conversations
    if (messages.length > 2) {
      saveChatToHistory();
    }
  }, [messages, sessionId]);

  // Clear chat session (always starts fresh now)
  const clearChatSession = () => {
    setMessages([
      { 
        text: "Hi! I'm your fashion assistant. What are you looking for today?\n\nChoose an option:\n• Browse Products - Search our collection\n• View Cart - Check your shopping cart\n• My Wishlist - See saved items\n• My Orders - View order history\n\nChoose query option:\n• Red dresses under ₹2000\n• Blue shirts for men\n• Black tops for women\n• White ethnic wear", 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: ["Browse Products", "View Cart", "My Wishlist", "My Orders", "Red dresses under ₹2000", "Blue shirts for men", "Black tops for women", "White ethnic wear"]
      },
    ]);
    console.log('Chat session cleared - starting fresh');
  };

  // Expose clearChatSession globally for logout functionality
  useEffect(() => {
    (window as any).clearFashionPulseChat = clearChatSession;
    
    // Also listen for logout events
    const handleLogout = () => {
      clearChatSession();
    };
    
    window.addEventListener('fashionpulse-logout', handleLogout);
    
    return () => {
      delete (window as any).clearFashionPulseChat;
      window.removeEventListener('fashionpulse-logout', handleLogout);
    };
  }, []); // Empty dependency array - this effect should only run once

  const sendMessageToAgent = async (message: string): Promise<{text: string, products: Product[], type?: string, action?: string}> => {
    try {
      const response = await fetch('http://localhost:5001/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return {
        text: data.response || "Sorry, I couldn't process your request right now.",
        products: data.products || [],
        type: data.type,
        action: data.action
      };
    } catch (error) {
      console.error('Chat API error:', error);
      
      // Check if it's a network error (server not running)
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        return {
          text: `🔌 **Connection Issue**

I'm having trouble connecting to the chat server. Please make sure:

1. **Chat Agent Server** is running on port 5001
2. **Start it with**: \`python chat_agent/api_server.py\`
3. **Check the terminal** for any error messages

💡 **Quick Fix**: Open a new terminal and run:
\`\`\`
python chat_agent/api_server.py
\`\`\`

Once the server is running, I'll be able to help you find products from our database! 🛍️`,
          products: []
        };
      }
      
      // Other errors
      return {
        text: `❌ **Error**: ${error instanceof Error ? error.message : 'Unknown error'}\n\nPlease try again or check if the chat server is running.`,
        products: [],
        type: 'error'
      };
    }
  };

  const handleSend = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage = inputText.trim();
    
    // Add user message
    setMessages((prev) => [...prev, { 
      text: userMessage, 
      isUser: true,
      timestamp: new Date().toISOString()
    }]);

    setInputText("");
    setIsLoading(true);

    try {
      // Prepare message with flow context if in a flow
      let messageWithContext = userMessage;
      if (currentFlow !== 'none') {
        messageWithContext = JSON.stringify({
          message: userMessage,
          flow: currentFlow,
          flowData: flowData
        });
      }

      // Get response from chat agent
      const agentResponse = await sendMessageToAgent(messageWithContext);
      
      // Handle special response types
      if (agentResponse.type === 'cart_request') {
        await handleCartRequest();
        return;
      } else if (agentResponse.type === 'wishlist_request') {
        await handleWishlistRequest();
        return;
      } else if (agentResponse.type === 'orders_request') {
        handleOrdersRequest();
        return;
      }
      
      // Add agent response
      setMessages((prev) => [...prev, { 
        text: agentResponse.text, 
        isUser: false,
        timestamp: new Date().toISOString(),
        products: agentResponse.products,
        type: agentResponse.type
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages((prev) => [...prev, { 
        text: "Sorry, I encountered an error. Please try again.", 
        isUser: false,
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleOptionClick = async (option: string) => {
    setIsLoading(true);
    
    try {
      if (option === "Face Tone Analysis" || option === "🎨" || option === "1️⃣ Face Tone") {
        // Start Face Tone flow with visual face tone selection
        setCurrentFlow('face_tone');
        setFlowData({ step: 'tone_selection' });
        
        setMessages((prev) => [...prev, { 
          text: "Perfect! Let's find colors that match your skin tone.\n\nChoose the shade that best matches your skin tone. I'll suggest colors that complement you perfectly!", 
          isUser: false,
          timestamp: new Date().toISOString(),
          options: ["Fair", "Wheatish", "Dusky", "Dark"]
        }]);
      } else if (option === "Body Fit Recommendations" || option === "👕" || option === "2️⃣ Body Fit") {
        // Start Body Fit flow with face icons for gender
        setCurrentFlow('body_fit');
        setFlowData({ step: 'gender_selection' });
        
        setMessages((prev) => [...prev, { 
          text: "Great choice! Let's find the perfect fit for you.\n\nFirst, please select your gender:", 
          isUser: false,
          timestamp: new Date().toISOString(),
          options: ["Men", "Women"]
        }]);
      } else if (option === "Calendar Event Planner" || option === "📅" || option === "3️⃣ Calendar") {
        // Start Calendar flow
        setShowCalendar(true);
        setCalendarStep('gender');
        
        setMessages((prev) => [...prev, { 
          text: "Perfect! Let's plan your outfits for upcoming events.\n\nI'll help you create calendar events and suggest perfect outfits for each occasion. Click the calendar button to get started!", 
          isUser: false,
          timestamp: new Date().toISOString()
        }]);
      } else if (option === "Browse Products") {
        setMessages((prev) => [...prev, { 
          text: "What type of products are you looking for? You can also type specific requests like 'red dresses under 2000' or 'blue shirts for men'.", 
          isUser: false,
          timestamp: new Date().toISOString(),
          options: ["Women's Clothing", "Men's Clothing", "Dresses", "Shirts", "Ethnic Wear"]
        }]);
      } else if (option === "View Cart") {
        await handleCartRequest();
        return;
      } else if (option === "My Wishlist") {
        await handleWishlistRequest();
        return;
      } else if (option === "My Orders") {
        handleOrdersRequest();
        return;
      } else if (option.includes("dresses under") || option.includes("shirts for") || option.includes("tops for") || option.includes("ethnic wear")) {
        // Handle specific query options
        const userMessage = option;
        
        // Add user message
        setMessages((prev) => [...prev, { 
          text: userMessage, 
          isUser: true,
          timestamp: new Date().toISOString()
        }]);

        // Get response from chat agent
        const agentResponse = await sendMessageToAgent(userMessage);
        
        // Add agent response
        setMessages((prev) => [...prev, { 
          text: agentResponse.text, 
          isUser: false,
          timestamp: new Date().toISOString(),
          products: agentResponse.products,
          type: agentResponse.type
        }]);
        
        setIsLoading(false);
        return;
      } else if (currentFlow === 'face_tone') {
        await handleFaceToneFlow(option);
      } else if (currentFlow === 'body_fit') {
        await handleBodyFitFlow(option);
      }
    } catch (error) {
      console.error('Error handling option click:', error);
      setMessages((prev) => [...prev, { 
        text: "Sorry, I encountered an error. Please try again.", 
        isUser: false,
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFaceToneFlow = async (option: string) => {
    const currentStep = flowData.step;
    
    if (currentStep === 'tone_selection') {
      // User selected face tone, suggest colors
      const colorSuggestions: { [key: string]: string[] } = {
        'Fair': ['Blue', 'Black'],
        'Wheatish': ['Red', 'Pink'], 
        'Dusky': ['White', 'Grey'],
        'Dark': ['Green', 'White', 'Blue']
      };
      
      const suggestedColors = colorSuggestions[option] || ['Blue', 'Black'];
      setFlowData({ ...flowData, selectedTone: option, step: 'color_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Excellent choice! For ${option} skin tone, these colors will look amazing on you:\n\n${suggestedColors.map((color: string) => `• ${color}`).join('\n')}\n\nPlease select one color:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: suggestedColors
      }]);
    } else if (currentStep === 'color_selection') {
      // User selected color, ask for gender
      setFlowData({ ...flowData, selectedColor: option, step: 'gender_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Perfect! ${option} is a great choice for you.\n\nNow please select your gender:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: ["Men", "Women"]
      }]);
    } else if (currentStep === 'gender_selection') {
      // User selected gender, show categories
      const categories = option === 'Men' 
        ? ['Shirts', 'T-shirts', 'Bottom Wear', 'Hoodies']
        : ['Western Wear', 'Dresses', 'Ethnic Wear', 'Tops and Co-ord Sets', "Women's Bottomwear"];
      
      setFlowData({ ...flowData, selectedGender: option, step: 'category_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Great! Now choose what type of ${option.toLowerCase()}'s clothing you're looking for:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: categories
      }]);
    } else if (currentStep === 'category_selection') {
      // User selected category, search products
      const { selectedColor, selectedGender } = flowData;
      
      try {
        const response = await fetch('http://localhost:5001/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: JSON.stringify({
              type: 'faceToneFlow',
              color: selectedColor,
              gender: selectedGender.toLowerCase(),
              category: option
            })
          })
        });
        
        const data = await response.json();
        
        setMessages((prev) => [...prev, { 
          text: `Perfect match! Here are ${selectedColor.toLowerCase()} ${option.toLowerCase()} for ${selectedGender.toLowerCase()} that will complement your ${flowData.selectedTone.toLowerCase()} skin tone:`, 
          isUser: false,
          timestamp: new Date().toISOString(),
          products: data.products || []
        }]);
        
        // Reset flow
        setCurrentFlow('none');
        setFlowData({});
      } catch (error) {
        console.error('Error fetching products:', error);
        setMessages((prev) => [...prev, { 
          text: "Sorry, I couldn't fetch products right now. Please try again later.", 
          isUser: false,
          timestamp: new Date().toISOString()
        }]);
      }
    }
  };

  const handleBodyFitFlow = async (option: string) => {
    const currentStep = flowData.step;
    
    if (currentStep === 'gender_selection') {
      // Show body shapes based on gender
      const bodyShapes = option === 'Men' 
        ? ['Rectangle', 'Triangle', 'Inverted Triangle', 'Oval', 'Trapezoid']
        : ['Hourglass', 'Pear', 'Apple', 'Rectangle', 'Inverted Triangle'];
      
      setFlowData({ ...flowData, selectedGender: option, step: 'body_shape_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Great! Now please select your body shape:\n\n${option === 'Men' ? 'Men\'s Body Shapes:' : 'Women\'s Body Shapes:'}`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: bodyShapes
      }]);
    } else if (currentStep === 'body_shape_selection') {
      // Get recommended categories based on body shape and gender
      const { selectedGender } = flowData;
      let recommendedCategories: string[] = [];
      
      if (selectedGender === 'Women') {
        const recommendations: { [key: string]: string[] } = {
          'Hourglass': ['Dresses', 'Western Wear', 'Tops and Co-ord Sets'],
          'Pear': ['Tops and Co-ord Sets', 'Western Wear', 'Ethnic Wear'],
          'Apple': ['Dresses', 'Tops and Co-ord Sets', 'Western Wear'],
          'Rectangle': ['Dresses', 'Western Wear', 'Ethnic Wear'],
          'Inverted Triangle': ['Dresses', 'Western Wear', 'Ethnic Wear']
        };
        recommendedCategories = recommendations[option] || ['Western Wear', 'Dresses', 'Ethnic Wear', 'Tops and Co-ord Sets'];
      } else {
        const recommendations: { [key: string]: string[] } = {
          'Rectangle': ['Shirts', 'T-shirts', 'Hoodies'],
          'Triangle': ['Shirts', 'Hoodies', 'T-shirts'],
          'Inverted Triangle': ['T-shirts', 'Shirts', 'Hoodies'],
          'Oval': ['Shirts', 'T-shirts', 'Hoodies'],
          'Trapezoid': ['Shirts', 'T-shirts', 'Hoodies']
        };
        recommendedCategories = recommendations[option] || ['Shirts', 'T-shirts', 'Hoodies'];
      }
      
      setFlowData({ ...flowData, selectedBodyShape: option, step: 'category_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Perfect! For your ${option.toLowerCase()} body shape, these categories will look amazing on you:\n\nRecommended for ${option} ${selectedGender.toLowerCase()}:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: recommendedCategories
      }]);
    } else if (currentStep === 'category_selection') {
      // User selected category, now ask for color
      setFlowData({ ...flowData, selectedCategory: option, step: 'color_selection' });
      
      setMessages((prev) => [...prev, { 
        text: `Excellent choice! ${option} will look great on your ${flowData.selectedBodyShape.toLowerCase()} body shape.\n\nNow choose your preferred color:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        options: ['Red', 'Blue', 'Black', 'White', 'Green', 'Pink', 'Grey', 'Yellow']
      }]);
    } else if (currentStep === 'color_selection') {
      // User selected color, search products
      const { selectedGender, selectedBodyShape, selectedCategory } = flowData;
      
      try {
        const response = await fetch('http://localhost:5001/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: JSON.stringify({
              type: 'bodyFitFlow',
              gender: selectedGender.toLowerCase(),
              bodyShape: selectedBodyShape,
              category: selectedCategory,
              color: option
            })
          })
        });
        
        const data = await response.json();
        
        setMessages((prev) => [...prev, { 
          text: data.response || `Perfect fit! Here are ${option.toLowerCase()} ${selectedCategory.toLowerCase()} that will look amazing on your ${selectedBodyShape.toLowerCase()} body shape:`, 
          isUser: false,
          timestamp: new Date().toISOString(),
          products: data.products || []
        }]);
        
        // Reset flow
        setCurrentFlow('none');
        setFlowData({});
      } catch (error) {
        console.error('Error fetching products:', error);
        setMessages((prev) => [...prev, { 
          text: "Sorry, I couldn't fetch products right now. Please try again later.", 
          isUser: false,
          timestamp: new Date().toISOString()
        }]);
      }
    }
  };

  const handleCartRequest = async () => {
    if (cart.length === 0) {
      setMessages((prev) => [...prev, { 
        text: "🛒 Your cart is empty! Start adding some amazing products to see them here.", 
        isUser: false,
        timestamp: new Date().toISOString(),
        type: 'cart_empty'
      }]);
    } else {
      // Fetch actual product details from backend for all cart items
      const cartProducts: Product[] = [];
      
      for (const item of cart) {
        try {
          const response = await fetch(`http://localhost:5000/api/products/${item.id}`);
          if (response.ok) {
            const productData = await response.json();
            cartProducts.push({
              product_id: String(item.id),
              product_name: item.title,
              price: item.price,
              product_image: item.image || productData.image_url || '',
              color: productData.color || '',
              gender: productData.gender || '',
              product_category: productData.product_category || 'Fashion',
              stock: item.qty,
              product_description: `Quantity: ${item.qty} | Total: ₹${item.price * item.qty}`
            });
          } else {
            // Fallback if API fails
            cartProducts.push({
              product_id: String(item.id),
              product_name: item.title,
              price: item.price,
              product_image: item.image || '',
              color: '',
              gender: '',
              product_category: 'Fashion',
              stock: item.qty,
              product_description: `Quantity: ${item.qty} | Total: ₹${item.price * item.qty}`
            });
          }
        } catch (error) {
          console.error('Error fetching product details for cart item:', error);
          // Fallback if network fails
          cartProducts.push({
            product_id: String(item.id),
            product_name: item.title,
            price: item.price,
            product_image: item.image || '',
            color: '',
            gender: '',
            product_category: 'Fashion',
            stock: item.qty,
            product_description: `Quantity: ${item.qty} | Total: ₹${item.price * item.qty}`
          });
        }
      }

      setMessages((prev) => [...prev, { 
        text: `🛒 **Your Cart (${cart.length} items)**\n\nTotal: ₹${cart.reduce((sum, item) => sum + (item.price * item.qty), 0)}\n\nClick any item to view details:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        products: cartProducts,
        type: 'cart_display'
      }]);
    }
  };

  const handleWishlistRequest = async () => {
    if (wishlist.length === 0) {
      setMessages((prev) => [...prev, { 
        text: "❤️ Your wishlist is empty! Save some products you love to see them here.", 
        isUser: false,
        timestamp: new Date().toISOString(),
        type: 'wishlist_empty'
      }]);
    } else {
      // Fetch actual product details from backend for all wishlist items
      const wishlistProducts: Product[] = [];
      
      for (const item of wishlist) {
        try {
          const response = await fetch(`http://localhost:5000/api/products/${item.id}`);
          if (response.ok) {
            const productData = await response.json();
            wishlistProducts.push({
              product_id: String(item.id),
              product_name: item.title,
              price: item.price || productData.price || 0,
              product_image: item.image || productData.image_url || '',
              color: productData.color || '',
              gender: productData.gender || '',
              product_category: productData.product_category || 'Fashion',
              stock: 1,
              product_description: 'Saved to your wishlist'
            });
          } else {
            // Fallback if API fails
            wishlistProducts.push({
              product_id: String(item.id),
              product_name: item.title,
              price: item.price || 0,
              product_image: item.image || '',
              color: '',
              gender: '',
              product_category: 'Fashion',
              stock: 1,
              product_description: 'Saved to your wishlist'
            });
          }
        } catch (error) {
          console.error('Error fetching product details for wishlist item:', error);
          // Fallback if network fails
          wishlistProducts.push({
            product_id: String(item.id),
            product_name: item.title,
            price: item.price || 0,
            product_image: item.image || '',
            color: '',
            gender: '',
            product_category: 'Fashion',
            stock: 1,
            product_description: 'Saved to your wishlist'
          });
        }
      }

      setMessages((prev) => [...prev, { 
        text: `❤️ **Your Wishlist (${wishlist.length} items)**\n\nYour saved favorites:\n\nClick any item to view details:`, 
        isUser: false,
        timestamp: new Date().toISOString(),
        products: wishlistProducts,
        type: 'wishlist_display'
      }]);
    }
  };

  const handleOrdersRequest = () => {
    try {
      const orders = JSON.parse(localStorage.getItem("orders") || "[]");
      
      if (orders.length === 0) {
        setMessages((prev) => [...prev, { 
          text: "📦 You haven't placed any orders yet! Start shopping to see your order history here.", 
          isUser: false,
          timestamp: new Date().toISOString(),
          type: 'orders_empty'
        }]);
      } else {
        const recentOrders = orders.slice(-5); // Show last 5 orders
        let orderText = `📦 **Your Recent Orders (${orders.length} total)**\n\n`;
        
        recentOrders.forEach((order: any, index: number) => {
          const orderDate = new Date(order.date).toLocaleDateString();
          const status = order.status === 'cancelled' ? '❌ Cancelled' : '✅ Confirmed';
          orderText += `**Order #${order.id}**\n`;
          orderText += `📅 ${orderDate} | ${status} | ₹${order.total}\n`;
          orderText += `📦 ${order.items.length} items\n\n`;
        });
        
        orderText += "💡 Go to 'My Orders' page for complete order management!";

        setMessages((prev) => [...prev, { 
          text: orderText, 
          isUser: false,
          timestamp: new Date().toISOString(),
          type: 'orders_display'
        }]);
      }
    } catch (error) {
      setMessages((prev) => [...prev, { 
        text: "❌ Unable to load order history. Please make sure you're logged in.", 
        isUser: false,
        timestamp: new Date().toISOString(),
        type: 'orders_error'
      }]);
    }
  };

  const formatMessage = (text: string) => {
    // Convert markdown-style formatting to HTML
    let formatted = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold
      .replace(/\n/g, '<br/>') // Line breaks
      .replace(/• /g, '• ') // Bullet points
      .replace(/(\d+)️⃣/g, '<span class="font-bold text-pink-600">$1️⃣</span>') // Numbered items
      .replace(/(💰|🎨|👤|📦|🏷️|🔍)/g, '<span class="inline-block mr-1">$1</span>'); // Emojis
    
    return formatted;
  };

  const [showNotification, setShowNotification] = useState(false);
  const [expandedMessages, setExpandedMessages] = useState<Set<number>>(new Set()); // Track which messages have expanded products
  const messagesEndRef = useRef<HTMLDivElement>(null); // Reference for auto-scroll

  const handleProductClick = (product: Product) => {
    // Store chat state before navigation
    const chatState = {
      isOpen: true,
      messages,
      timestamp: new Date().toISOString()
    };
    sessionStorage.setItem('fashionpulse_chat_return', JSON.stringify(chatState));
    
    // Navigate to product page (same tab, so back button works)
    window.location.href = `/products/${product.product_id}`;
  };

  const renderProductCard = (product: Product, index: number) => (
    <div 
      key={product.product_id} 
      className="bg-white rounded-xl border-2 border-pink-200 overflow-hidden shadow-lg hover:shadow-xl transition-all cursor-pointer transform hover:scale-102 hover:border-pink-400"
      onClick={() => handleProductClick(product)}
    >
      {/* Product Image */}
      <div className="aspect-square bg-gradient-to-br from-pink-50 to-purple-50 relative">
        <img
          src={product.product_image}
          alt={product.product_name}
          className="w-full h-full object-cover"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.src = `https://via.placeholder.com/300x300/ec4899/ffffff?text=${encodeURIComponent(product.product_name.substring(0, 15))}`;
          }}
        />
        <div className="absolute top-3 left-3 bg-pink-500 text-white text-sm px-3 py-1 rounded-full font-bold shadow-lg">
          #{index + 1}
        </div>
        <div className="absolute top-3 right-3 bg-white/90 backdrop-blur-sm text-pink-600 text-xs px-2 py-1 rounded-full font-medium">
          🏷️ {product.product_category}
        </div>
      </div>
      
      {/* Product Details */}
      <div className="p-4">
        {/* Product Name */}
        <h4 className="font-bold text-base text-gray-900 mb-2 line-clamp-2 hover:text-pink-600 transition-colors leading-tight">
          {product.product_name}
        </h4>
        
        {/* Product Description */}
        <p className="text-sm text-gray-600 mb-3 line-clamp-2 leading-relaxed">
          {product.product_description || 'Premium quality clothing item crafted with attention to detail. Perfect for style-conscious individuals who value comfort and elegance.'}
        </p>
        
        {/* Color and Gender Row */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <div className="flex items-center text-sm">
              <span 
                className="w-4 h-4 rounded-full border-2 border-gray-300 mr-2 shadow-sm" 
                style={{backgroundColor: 
                  product.color.toLowerCase() === 'red' ? '#ef4444' : 
                  product.color.toLowerCase() === 'blue' ? '#3b82f6' :
                  product.color.toLowerCase() === 'black' ? '#1f2937' :
                  product.color.toLowerCase() === 'white' ? '#f9fafb' :
                  product.color.toLowerCase() === 'green' ? '#10b981' :
                  product.color.toLowerCase() === 'yellow' ? '#f59e0b' :
                  product.color.toLowerCase() === 'pink' ? '#ec4899' :
                  product.color.toLowerCase() === 'purple' ? '#8b5cf6' :
                  product.color.toLowerCase() === 'brown' ? '#92400e' :
                  product.color.toLowerCase() === 'grey' || product.color.toLowerCase() === 'gray' ? '#6b7280' :
                  '#6b7280'
                }}
              ></span>
              <span className="text-gray-700 font-medium capitalize">{product.color}</span>
            </div>
          </div>
          <div className="flex items-center text-sm text-gray-600">
            <span className="mr-1">
              {product.gender.toLowerCase() === 'men' ? '👨' : 
               product.gender.toLowerCase() === 'women' ? '👩' : 
               product.gender.toLowerCase().includes('kid') ? '👶' : '👤'}
            </span>
            <span className="font-medium capitalize">{product.gender}</span>
          </div>
        </div>
        
        {/* Price Row (removed stock) */}
        <div className="flex items-center justify-between mb-3">
          <div className="text-left">
            <span className="text-2xl font-bold text-pink-600">₹{product.price.toLocaleString()}</span>
          </div>
        </div>
        
        {/* Action Button */}
        <div className="mt-4 pt-3 border-t border-pink-100">
          <div className="flex items-center justify-center text-pink-600 font-semibold text-sm hover:text-pink-700 transition-colors">
            <span className="mr-2">👆</span>
            <span>Click to view full details</span>
            <span className="ml-2">🔗</span>
          </div>
        </div>
      </div>
    </div>
  );

  const renderMessage = (msg: Message, messageIndex: number) => {
    // Check if message has products to display
    const hasProducts = msg.products && msg.products.length > 0;
    
    if (hasProducts && !msg.isUser) {
      const isExpanded = expandedMessages.has(messageIndex);
      const productsToShow = isExpanded ? msg.products! : msg.products!.slice(0, 2);
      const hasMoreProducts = msg.products!.length > 2;
      
      return (
        <div className="space-y-3">
          <div 
            className="text-sm leading-relaxed"
            dangerouslySetInnerHTML={{ __html: formatMessage(msg.text) }}
          />
          
          {/* Product Grid */}
          <div className="space-y-4 mt-4">
            {productsToShow.map((product, index) => renderProductCard(product, index))}
          </div>
          
          {/* View All / Show Less Button */}
          {hasMoreProducts && (
            <div className="text-center mt-4">
              {!isExpanded ? (
                <button
                  onClick={() => {
                    setExpandedMessages(prev => new Set([...prev, messageIndex]));
                  }}
                  className="bg-gradient-to-r from-pink-400 to-pink-500 text-white px-6 py-3 rounded-full hover:from-pink-500 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl font-semibold text-sm flex items-center gap-2 mx-auto"
                >
                  <span>👀</span>
                  <span>View All {msg.products!.length} Products</span>
                  <span>📦</span>
                </button>
              ) : (
                <div className="space-y-3">
                  <div className="text-sm text-gray-600 text-center p-3 bg-green-50 rounded-lg border border-green-200">
                    <span className="font-medium">✅ Showing all {msg.products!.length} products</span>
                  </div>
                  <button
                    onClick={() => {
                      setExpandedMessages(prev => {
                        const newSet = new Set(prev);
                        newSet.delete(messageIndex);
                        return newSet;
                      });
                    }}
                    className="bg-gradient-to-r from-gray-400 to-gray-500 text-white px-6 py-2 rounded-full hover:from-gray-500 hover:to-gray-600 transition-all shadow-lg font-semibold text-sm flex items-center gap-2 mx-auto"
                  >
                    <span>🔼</span>
                    <span>Show Less</span>
                  </button>
                </div>
              )}
            </div>
          )}
          
          <div className={`text-xs opacity-70 text-gray-500`}>
            {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </div>
        </div>
      );
    }
    
    // Regular message formatting
    return (
      <div>
        <div 
          className="text-sm leading-relaxed"
          dangerouslySetInnerHTML={{ __html: formatMessage(msg.text) }}
        />
        
        {/* Option buttons */}
        {msg.options && msg.options.length > 0 && !msg.isUser && (
          <div className="mt-3 flex flex-wrap gap-2">
            {msg.options.map((option, index) => {
              // Check if this is a Face Tone selection (skin tone circles)
              const isFaceToneSelection = ['Fair', 'Wheatish', 'Dusky', 'Dark'].includes(option);
              
              // Check if this is a color suggestion (colored buttons)
              const isColorSuggestion = msg.text.includes('these colors will look amazing') || 
                                      msg.text.includes('Excellent choice!') ||
                                      msg.text.includes('Please select one color');
              
              if (isFaceToneSelection) {
                // Skin tone colors for circles
                const skinToneColors: { [key: string]: string } = {
                  'Fair': '#fdbcb4',      // Light peachy pink
                  'Wheatish': '#deb887',  // Burlywood
                  'Dusky': '#cd853f',     // Peru brown
                  'Dark': '#8b4513'       // Saddle brown
                };
                
                return (
                  <button
                    key={index}
                    onClick={() => handleOptionClick(option)}
                    disabled={isLoading}
                    className="flex flex-col items-center gap-2 p-3 rounded-lg hover:bg-gray-50 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <div 
                      className="w-12 h-12 rounded-full border-3 border-gray-300 hover:border-pink-400 transition-colors shadow-md"
                      style={{ backgroundColor: skinToneColors[option] }}
                    ></div>
                    <span className="text-sm font-medium text-gray-700">{option}</span>
                  </button>
                );
              } else if (isColorSuggestion) {
                // Color suggestion buttons with actual colors
                const colorStyles: { [key: string]: { bg: string, text: string, border: string } } = {
                  'Blue': { bg: '#3b82f6', text: 'white', border: '#1d4ed8' },
                  'Black': { bg: '#1f2937', text: 'white', border: '#111827' },
                  'Red': { bg: '#ef4444', text: 'white', border: '#dc2626' },
                  'Pink': { bg: '#ec4899', text: 'white', border: '#db2777' },
                  'White': { bg: '#ffffff', text: '#1f2937', border: '#d1d5db' },
                  'Grey': { bg: '#6b7280', text: 'white', border: '#4b5563' },
                  'Green': { bg: '#10b981', text: 'white', border: '#059669' }
                };
                
                const colorStyle = colorStyles[option] || { bg: '#ec4899', text: 'white', border: '#db2777' };
                
                return (
                  <button
                    key={index}
                    onClick={() => handleOptionClick(option)}
                    disabled={isLoading}
                    className="px-6 py-3 rounded-full font-medium text-sm transition-all shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105"
                    style={{ 
                      backgroundColor: colorStyle.bg, 
                      color: colorStyle.text,
                      border: `2px solid ${colorStyle.border}`
                    }}
                  >
                    {option}
                  </button>
                );
              } else {
                // Default pink buttons for other options
                return (
                  <button
                    key={index}
                    onClick={() => handleOptionClick(option)}
                    disabled={isLoading}
                    className="bg-gradient-to-r from-pink-400 to-pink-500 text-white px-4 py-2 rounded-full hover:from-pink-500 hover:to-pink-600 transition-all shadow-md hover:shadow-lg font-medium text-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {option}
                  </button>
                );
              }
            })}
          </div>
        )}
        
        <div className={`text-xs mt-1 opacity-70 ${msg.isUser ? 'text-white/70' : 'text-gray-500'}`}>
          {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>
    );
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="bg-white rounded-2xl shadow-2xl w-96 sm:w-[500px] h-[650px] flex flex-col overflow-hidden border-2 border-pink-300">
          {/* Header */}
          <div className="bg-gradient-to-r from-pink-400 to-pink-500 p-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center">
                <svg className="w-9 h-9" viewBox="0 0 100 100" fill="none">
                  {/* Robot head */}
                  <rect x="25" y="35" width="50" height="45" rx="8" fill="#f5f1e8" stroke="#ec4899" strokeWidth="2"/>
                  {/* Antenna */}
                  <line x1="50" y1="35" x2="50" y2="25" stroke="#ec4899" strokeWidth="3" strokeLinecap="round"/>
                  <circle cx="50" cy="22" r="4" fill="#fcd705ff"/>
                  {/* Eyes */}
                  <circle cx="38" cy="50" r="5" fill="#ec4899"/>
                  <circle cx="62" cy="50" r="5" fill="#ec4899"/>
                  <circle cx="40" cy="48" r="2" fill="white"/>
                  <circle cx="64" cy="48" r="2" fill="white"/>
                  {/* Cute smile */}
                  <path d="M35 65 Q50 72 65 65" stroke="#ec4899" strokeWidth="3" strokeLinecap="round" fill="none"/>
                  {/* Rosy cheeks */}
                  <circle cx="28" cy="60" r="4" fill="#FFB6C1" opacity="0.6"/>
                  <circle cx="72" cy="60" r="4" fill="#FFB6C1" opacity="0.6"/>
                  {/* Ears */}
                  <rect x="18" y="45" width="6" height="15" rx="3" fill="#ec4899"/>
                  <rect x="76" y="45" width="6" height="15" rx="3" fill="#ec4899"/>
                </svg>
              </div>
              <div>
                <h3 className="text-white font-bold">Style Assistant</h3>
                <p className="text-white/80 text-xs">Connected to FashionPulse DB</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {/* Face Tone Icon */}
              <button
                onClick={() => handleOptionClick("🎨")}
                className="text-white/80 hover:text-white text-xl p-1 rounded hover:bg-white/10 transition-colors"
                title="Face Tone Analysis"
              >
                🎨
              </button>
              
              {/* Body Fit Icon */}
              <button
                onClick={() => handleOptionClick("👕")}
                className="text-white/80 hover:text-white text-xl p-1 rounded hover:bg-white/10 transition-colors"
                title="Body Fit Analysis"
              >
                👕
              </button>
              
              {/* Three dots menu */}
              <div className="relative">
                <button
                  onClick={() => setShowDropdown(!showDropdown)}
                  className="text-white/80 hover:text-white text-xl p-1 rounded hover:bg-white/10 transition-colors"
                  title="Menu"
                >
                  ⋯
                </button>
                {showDropdown && (
                  <div className="absolute right-0 top-full mt-2 bg-white rounded-lg shadow-lg border border-gray-200 min-w-[150px] z-50">
                    <button
                      onClick={() => {
                        resetChatToInitialState();
                        setShowDropdown(false);
                      }}
                      className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-t-lg flex items-center gap-2"
                    >
                      💬 New Chat
                    </button>
                    <button
                      onClick={() => handleDropdownAction('history')}
                      className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                    >
                      📜 History
                    </button>
                    <button
                      onClick={() => handleDropdownAction('features')}
                      className="w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100 rounded-b-lg flex items-center gap-2"
                    >
                      ⭐ Features
                    </button>
                  </div>
                )}
              </div>
              
              <button
                onClick={() => setIsOpen(false)}
                className="text-white hover:text-white/80 text-2xl font-bold"
              >
                ✕
              </button>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 p-4 space-y-3 overflow-y-auto max-h-[550px] bg-gray-50 scroll-smooth">
            {/* History Overlay - Full Screen */}
            {showHistory && (
              <div className="absolute inset-0 bg-white z-50 flex flex-col">
                {/* Header */}
                <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">📜</span>
                    <h3 className="text-xl font-bold text-white">Chat History</h3>
                  </div>
                  <button
                    onClick={() => setShowHistory(false)}
                    className="text-white hover:text-gray-200 text-2xl font-bold bg-white/20 rounded-full w-8 h-8 flex items-center justify-center"
                  >
                    ✕
                  </button>
                </div>
                
                {/* Content */}
                <div className="flex-1 p-4 overflow-y-auto">
                  {chatHistory.length === 0 ? (
                    <div className="text-center py-16">
                      <div className="text-6xl mb-4">💬</div>
                      <h4 className="text-xl font-semibold text-gray-700 mb-2">No Chat History Yet</h4>
                      <p className="text-gray-500 mb-6">Start chatting to see your conversation history here!</p>
                      <div className="bg-gradient-to-r from-pink-100 to-purple-100 rounded-lg p-4 max-w-md mx-auto">
                        <p className="text-sm text-gray-600">
                          💡 <strong>Tip:</strong> Your chat history is automatically saved and you can revisit any previous conversation anytime.
                        </p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="bg-gradient-to-r from-pink-50 to-purple-50 rounded-lg p-4 mb-6">
                        <h4 className="font-semibold text-gray-800 mb-2">📊 Your Chat Statistics</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div className="text-center">
                            <div className="text-2xl font-bold text-pink-600">{chatHistory.length}</div>
                            <div className="text-gray-600">Total Chats</div>
                          </div>
                          <div className="text-center">
                            <div className="text-2xl font-bold text-purple-600">
                              {chatHistory.reduce((sum, chat) => sum + chat.messages.length, 0)}
                            </div>
                            <div className="text-gray-600">Total Messages</div>
                          </div>
                        </div>
                      </div>
                      
                      <h4 className="font-semibold text-gray-800 mb-3">Recent Conversations</h4>
                      <div className="grid gap-3">
                        {chatHistory.map((chat, index) => (
                          <div
                            key={`${chat.id}_${index}`}
                            onClick={() => loadHistoryChat(chat)}
                            className="bg-white rounded-xl p-4 cursor-pointer hover:shadow-lg transition-all border-2 border-gray-100 hover:border-pink-200 group"
                          >
                            <div className="flex justify-between items-start mb-3">
                              <div className="flex items-center gap-2">
                                <span className="text-lg">💬</span>
                                <h5 className="font-semibold text-gray-800 group-hover:text-pink-600 transition-colors">
                                  {chat.title}
                                </h5>
                              </div>
                              <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                                {new Date(chat.timestamp).toLocaleDateString()}
                              </span>
                            </div>
                            
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-4 text-sm text-gray-600">
                                <span className="flex items-center gap-1">
                                  <span>💭</span>
                                  {chat.messages.length} messages
                                </span>
                                <span className="flex items-center gap-1">
                                  <span>⏰</span>
                                  {new Date(chat.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                              </div>
                              <span className="text-pink-500 opacity-0 group-hover:opacity-100 transition-opacity">
                                Click to load →
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Features Overlay - Full Screen */}
            {showFeatures && (
              <div className="absolute inset-0 bg-white z-50 flex flex-col">
                {/* Header */}
                <div className="bg-gradient-to-r from-blue-500 to-purple-500 p-4 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">⭐</span>
                    <h3 className="text-xl font-bold text-white">AI Features</h3>
                  </div>
                  <button
                    onClick={() => setShowFeatures(false)}
                    className="text-white hover:text-gray-200 text-2xl font-bold bg-white/20 rounded-full w-8 h-8 flex items-center justify-center"
                  >
                    ✕
                  </button>
                </div>
                
                {/* Content */}
                <div className="flex-1 p-4 overflow-y-auto">
                  <div className="max-w-2xl mx-auto">
                    {/* Introduction */}
                    <div className="text-center mb-8">
                      <div className="text-6xl mb-4">🤖</div>
                      <h4 className="text-2xl font-bold text-gray-800 mb-2">AI-Powered Fashion Assistant</h4>
                      <p className="text-gray-600">Discover personalized fashion recommendations with our intelligent features</p>
                    </div>

                    {/* Features Grid */}
                    <div className="space-y-6">
                      {/* Face Tone Feature */}
                      <div className="bg-gradient-to-br from-pink-50 to-rose-100 rounded-2xl p-6 border-2 border-pink-200 hover:border-pink-300 transition-colors">
                        <div className="flex items-start gap-4">
                          <div className="bg-pink-500 rounded-full p-3 text-white text-2xl">🎨</div>
                          <div className="flex-1">
                            <h4 className="text-xl font-bold text-pink-800 mb-2">Face Tone Analysis</h4>
                            <p className="text-pink-700 mb-4">
                              Get personalized color recommendations based on your unique skin tone. Our AI analyzes your complexion to suggest the most flattering colors.
                            </p>
                            
                            <div className="bg-white/60 rounded-lg p-4 mb-4">
                              <h5 className="font-semibold text-pink-800 mb-2">How it works:</h5>
                              <div className="space-y-2 text-sm text-pink-700">
                                <div className="flex items-center gap-2">
                                  <span className="bg-pink-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">1</span>
                                  Select your skin tone (Fair, Wheatish, Dusky, Dark)
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-pink-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">2</span>
                                  Choose from AI-suggested complementary colors
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-pink-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">3</span>
                                  Select your gender and preferred category
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-pink-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">4</span>
                                  Discover perfectly matched products
                                </div>
                              </div>
                            </div>
                            
                            <button
                              onClick={() => {
                                setShowFeatures(false);
                                handleOptionClick("🎨");
                              }}
                              className="bg-gradient-to-r from-pink-500 to-rose-500 text-white px-6 py-3 rounded-full font-semibold hover:from-pink-600 hover:to-rose-600 transition-all shadow-lg hover:shadow-xl"
                            >
                              ✨ Try Face Tone Analysis
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Body Fit Feature */}
                      <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl p-6 border-2 border-blue-200 hover:border-blue-300 transition-colors">
                        <div className="flex items-start gap-4">
                          <div className="bg-blue-500 rounded-full p-3 text-white text-2xl">👕</div>
                          <div className="flex-1">
                            <h4 className="text-xl font-bold text-blue-800 mb-2">Body Fit Recommendations</h4>
                            <p className="text-blue-700 mb-4">
                              Find clothes that perfectly complement your body shape. Our intelligent system recommends the most flattering styles for your unique physique.
                            </p>
                            
                            <div className="bg-white/60 rounded-lg p-4 mb-4">
                              <h5 className="font-semibold text-blue-800 mb-2">Smart recommendations for:</h5>
                              <div className="grid grid-cols-2 gap-3 text-sm text-blue-700">
                                <div>
                                  <strong>Women:</strong>
                                  <div className="text-xs mt-1 space-y-1">
                                    <div>⏳ Hourglass • 🍐 Pear</div>
                                    <div>🍎 Apple • 📐 Rectangle</div>
                                    <div>🔻 Inverted Triangle</div>
                                  </div>
                                </div>
                                <div>
                                  <strong>Men:</strong>
                                  <div className="text-xs mt-1 space-y-1">
                                    <div>📐 Rectangle • 🔺 Triangle</div>
                                    <div>🔻 Inverted Triangle</div>
                                    <div>⭕ Oval • 🏠 Trapezoid</div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            
                            <div className="bg-white/60 rounded-lg p-4 mb-4">
                              <h5 className="font-semibold text-blue-800 mb-2">Process:</h5>
                              <div className="space-y-2 text-sm text-blue-700">
                                <div className="flex items-center gap-2">
                                  <span className="bg-blue-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">1</span>
                                  Select your gender and body shape
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-blue-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">2</span>
                                  Get intelligent category recommendations
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-blue-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">3</span>
                                  Choose your preferred color
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-blue-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">4</span>
                                  View perfectly fitted products
                                </div>
                              </div>
                            </div>
                            
                            <button
                              onClick={() => {
                                setShowFeatures(false);
                                handleOptionClick("👕");
                              }}
                              className="bg-gradient-to-r from-blue-500 to-indigo-500 text-white px-6 py-3 rounded-full font-semibold hover:from-blue-600 hover:to-indigo-600 transition-all shadow-lg hover:shadow-xl"
                            >
                              👔 Try Body Fit Analysis
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Calendar Feature */}
                      <div className="bg-gradient-to-br from-green-50 to-emerald-100 rounded-2xl p-6 border-2 border-green-200 hover:border-green-300 transition-colors">
                        <div className="flex items-start gap-4">
                          <div className="bg-green-500 rounded-full p-3 text-white text-2xl">📅</div>
                          <div className="flex-1">
                            <h4 className="text-xl font-bold text-green-800 mb-2">Calendar Event Planner</h4>
                            <p className="text-green-700 mb-4">
                              Plan your outfits for upcoming events! Get personalized outfit recommendations based on your calendar events, weather, and occasion type.
                            </p>
                            
                            <div className="bg-white/60 rounded-lg p-4 mb-4">
                              <h5 className="font-semibold text-green-800 mb-2">Perfect for:</h5>
                              <div className="grid grid-cols-2 gap-3 text-sm text-green-700">
                                <div>
                                  <strong>Events:</strong>
                                  <div className="text-xs mt-1 space-y-1">
                                    <div>💼 Business Meetings</div>
                                    <div>🎉 Parties & Celebrations</div>
                                    <div>💒 Weddings & Ceremonies</div>
                                  </div>
                                </div>
                                <div>
                                  <strong>Occasions:</strong>
                                  <div className="text-xs mt-1 space-y-1">
                                    <div>🌅 Morning Events</div>
                                    <div>🌆 Evening Functions</div>
                                    <div>🎭 Special Occasions</div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            
                            <div className="bg-white/60 rounded-lg p-4 mb-4">
                              <h5 className="font-semibold text-green-800 mb-2">How it works:</h5>
                              <div className="space-y-2 text-sm text-green-700">
                                <div className="flex items-center gap-2">
                                  <span className="bg-green-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">1</span>
                                  Select your gender and event date
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-green-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">2</span>
                                  Choose event type or add custom event
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-green-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">3</span>
                                  Get AI-powered outfit suggestions
                                </div>
                                <div className="flex items-center gap-2">
                                  <span className="bg-green-200 rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">4</span>
                                  Save events and get reminders
                                </div>
                              </div>
                            </div>
                            
                            <button
                              onClick={() => {
                                setShowFeatures(false);
                                handleOptionClick("📅");
                              }}
                              className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-6 py-3 rounded-full font-semibold hover:from-green-600 hover:to-emerald-600 transition-all shadow-lg hover:shadow-xl"
                            >
                              📅 Plan Your Outfits
                            </button>
                          </div>
                        </div>
                      </div>

                      {/* Additional Info */}
                      <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl p-4 border border-purple-200">
                        <div className="text-center">
                          <span className="text-2xl mb-2 block">💡</span>
                          <h5 className="font-semibold text-purple-800 mb-1">Pro Tip</h5>
                          <p className="text-sm text-purple-700">
                            Combine both features for the ultimate personalized shopping experience! Use Face Tone for colors and Body Fit for styles.
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Regular Messages */}
            {!showHistory && !showFeatures && (
              <>
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.isUser ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                        msg.isUser
                          ? "bg-gradient-to-r from-pink-400 to-pink-500 text-white rounded-br-none"
                          : "bg-white text-gray-800 shadow-md rounded-bl-none border border-gray-200"
                      }`}
                    >
                      {renderMessage(msg, idx)}
                    </div>
                  </div>
                ))}
                
                {/* Loading indicator */}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white text-gray-800 shadow-md rounded-2xl rounded-bl-none px-4 py-3 border border-gray-200">
                      <div className="flex items-center gap-2">
                        <div className="flex space-x-1">
                          <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-pink-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                        <span className="text-xs text-gray-500">Searching products...</span>
                      </div>
                    </div>
                  </div>
                )}

                {/* Auto-scroll reference */}
                <div ref={messagesEndRef} />

                {/* Product opened notification */}
                {showNotification && (
                  <div className="flex justify-center mb-2">
                    <div className="bg-green-100 border border-green-300 text-green-800 px-4 py-2 rounded-lg shadow-sm animate-pulse">
                      <div className="flex items-center gap-2 text-sm">
                        <span>🔗</span>
                        <span>Product opened in new tab! Chat remains available.</span>
                      </div>
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
          
          {/* Input */}
          <div className="p-4 bg-white border-t border-gray-200">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleSend()}
                placeholder="Try: 'Show me red dresses under ₹2000'"
                disabled={isLoading}
                className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-pink-400 text-sm text-black placeholder-gray-500 bg-white disabled:opacity-50"
                style={{ color: '#000000' }}
              />
              
              {/* Calendar Icon */}
              <button
                onClick={handleCalendarClick}
                disabled={isLoading}
                className={`p-3 rounded-full transition-all shadow-lg hover:shadow-xl font-bold disabled:opacity-50 disabled:cursor-not-allowed ${
                  hasUpcomingEvents 
                    ? 'bg-gradient-to-r from-orange-400 to-red-500 text-white animate-pulse' 
                    : 'bg-gradient-to-r from-purple-400 to-purple-500 text-white hover:from-purple-500 hover:to-purple-600'
                }`}
                title={hasUpcomingEvents ? "You have upcoming events!" : "Add Calendar Event"}
              >
                📅
              </button>
              
              <button
                onClick={handleSend}
                disabled={isLoading || !inputText.trim()}
                className="bg-gradient-to-r from-pink-400 to-pink-500 text-white rounded-full px-5 py-3 hover:from-pink-500 hover:to-pink-600 transition-all shadow-lg hover:shadow-xl font-bold disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? "..." : "➤"}
              </button>
            </div>
            
            {/* Calendar Popup */}
            {showCalendar && (
              <div className="absolute inset-0 bg-black/50 z-60 flex items-center justify-center p-4">
                <div className="bg-white rounded-2xl shadow-2xl max-w-md w-full max-h-[80vh] overflow-y-auto">
                  {/* Header */}
                  <div className="bg-gradient-to-r from-purple-500 to-pink-500 p-4 rounded-t-2xl">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        {calendarStep !== 'gender' && (
                          <button
                            onClick={() => {
                              if (calendarStep === 'date') {
                                setCalendarStep('gender');
                              } else if (calendarStep === 'event') {
                                setCalendarStep('date');
                              }
                            }}
                            className="text-white hover:text-gray-200 text-xl font-bold bg-white/20 rounded-full w-8 h-8 flex items-center justify-center"
                            title="Back"
                          >
                            ←
                          </button>
                        )}
                        <span className="text-2xl">📅</span>
                        <h3 className="text-xl font-bold text-white">Add Event</h3>
                      </div>
                      <button
                        onClick={() => {
                          setShowCalendar(false);
                          setCalendarStep('gender');
                          setCalendarData({});
                        }}
                        className="text-white hover:text-gray-200 text-2xl font-bold bg-white/20 rounded-full w-8 h-8 flex items-center justify-center"
                      >
                        ✕
                      </button>
                    </div>
                    
                    {/* Progress Indicator */}
                    <div className="flex items-center justify-center mt-3 gap-2">
                      <div className={`w-3 h-3 rounded-full ${calendarStep === 'gender' ? 'bg-white' : 'bg-white/40'}`}></div>
                      <div className={`w-3 h-3 rounded-full ${calendarStep === 'date' ? 'bg-white' : 'bg-white/40'}`}></div>
                      <div className={`w-3 h-3 rounded-full ${calendarStep === 'event' ? 'bg-white' : 'bg-white/40'}`}></div>
                    </div>
                  </div>
                  
                  {/* Content */}
                  <div className="p-6">
                    {calendarStep === 'gender' && (
                      <div className="text-center">
                        <div className="text-4xl mb-4">👤</div>
                        <h4 className="text-xl font-bold text-gray-800 mb-2">Select Your Gender</h4>
                        <p className="text-gray-600 mb-6">This helps us suggest the perfect outfits for your event</p>
                        
                        <div className="space-y-3">
                          <button
                            onClick={() => handleCalendarStep('Women')}
                            className="w-full bg-gradient-to-r from-pink-100 to-rose-100 hover:from-pink-200 hover:to-rose-200 border-2 border-pink-300 rounded-xl p-4 transition-all"
                          >
                            <div className="flex items-center justify-center gap-3">
                              <span className="text-2xl">👩</span>
                              <span className="font-semibold text-pink-800">Women</span>
                            </div>
                          </button>
                          
                          <button
                            onClick={() => handleCalendarStep('Men')}
                            className="w-full bg-gradient-to-r from-blue-100 to-indigo-100 hover:from-blue-200 hover:to-indigo-200 border-2 border-blue-300 rounded-xl p-4 transition-all"
                          >
                            <div className="flex items-center justify-center gap-3">
                              <span className="text-2xl">👨</span>
                              <span className="font-semibold text-blue-800">Men</span>
                            </div>
                          </button>
                        </div>
                      </div>
                    )}
                    
                    {calendarStep === 'date' && (
                      <div className="text-center">
                        <div className="text-4xl mb-4">📅</div>
                        <h4 className="text-xl font-bold text-gray-800 mb-2">Select Event Date</h4>
                        <p className="text-gray-600 mb-6">Choose when your event is happening</p>
                        
                        {/* Custom Calendar Component */}
                        <div className="bg-gray-50 rounded-xl p-4 mb-4">
                          <CustomCalendar 
                            onDateSelect={handleDateSelection}
                            selectedDate={calendarData.date}
                          />
                        </div>
                        
                        {/* Selected Date Display */}
                        {calendarData.date && (
                          <div className="bg-white border-2 border-purple-300 rounded-xl p-4 mb-4">
                            <div className="text-sm text-gray-600 mb-1">Selected Date:</div>
                            <div className="text-lg font-bold text-black">
                              {new Date(calendarData.date).toLocaleDateString('en-US', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                              })}
                            </div>
                            <button
                              onClick={() => setCalendarStep('event')}
                              className="mt-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-2 rounded-full font-semibold hover:from-purple-600 hover:to-pink-600 transition-all"
                            >
                              Next: Add Event →
                            </button>
                          </div>
                        )}
                        
                        {/* Quick Date Options */}
                        <div className="space-y-2">
                          <div className="grid grid-cols-2 gap-2">
                            {[
                              { label: 'Tomorrow', days: 1 },
                              { label: 'Next Week', days: 7 },
                              { label: 'Next Month', days: 30 },
                              { label: 'In 3 Months', days: 90 }
                            ].map((option) => {
                              const futureDate = new Date();
                              futureDate.setDate(futureDate.getDate() + option.days);
                              const dateString = futureDate.toISOString().split('T')[0];
                              
                              return (
                                <button
                                  key={option.label}
                                  onClick={() => {
                                    setCalendarData({ ...calendarData, date: dateString });
                                  }}
                                  className="bg-white border-2 border-purple-200 hover:border-purple-400 rounded-lg p-3 text-sm font-medium transition-all hover:bg-purple-50"
                                >
                                  {option.label}
                                  <div className="text-xs text-gray-500 mt-1">
                                    {futureDate.toLocaleDateString()}
                                  </div>
                                </button>
                              );
                            })}
                          </div>
                        </div>
                      </div>
                    )}
                    
                    {calendarStep === 'event' && (
                      <div className="text-center">
                        <div className="text-4xl mb-4">🎉</div>
                        <h4 className="text-xl font-bold text-gray-800 mb-2">What's the Event?</h4>
                        <p className="text-gray-600 mb-6">Select or type your event type</p>
                        
                        {!showCustomEventInput ? (
                          <>
                            <div className="grid grid-cols-2 gap-3 mb-4">
                              {[
                                'Job Interview',
                                'Wedding',
                                'Birthday',
                                'Festival',
                                'Party',
                                'Travel',
                                'Meeting',
                                'College',
                                'Temple',
                                'Family Function',
                                'Night Out',
                                'Photoshoot'
                              ].map((event) => (
                                <button
                                  key={event}
                                  onClick={() => handleCalendarStep(event)}
                                  className="bg-gradient-to-r from-purple-50 to-pink-50 hover:from-purple-100 hover:to-pink-100 border-2 border-purple-200 hover:border-purple-300 rounded-lg p-3 transition-all text-sm font-medium"
                                >
                                  {event}
                                </button>
                              ))}
                            </div>
                            
                            {/* Others Option */}
                            <button
                              onClick={() => setShowCustomEventInput(true)}
                              className="w-full bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 border-2 border-gray-300 hover:border-gray-400 rounded-lg p-4 transition-all font-medium text-gray-700 mb-4"
                            >
                              Others (Custom Event)
                            </button>
                          </>
                        ) : (
                          <div className="space-y-4">
                            <div className="bg-gray-50 rounded-xl p-4">
                              <label className="block text-sm font-medium text-gray-700 mb-2">
                                Enter your custom event:
                              </label>
                              <input
                                type="text"
                                placeholder="e.g., Date Night, Graduation, Conference..."
                                className="w-full p-3 border-2 border-gray-300 rounded-xl focus:outline-none focus:border-purple-500 text-black font-medium"
                                onKeyDown={(e) => {
                                  if (e.key === 'Enter' && (e.target as HTMLInputElement).value.trim()) {
                                    handleCustomEventSave((e.target as HTMLInputElement).value.trim());
                                  }
                                }}
                                autoFocus
                              />
                              <div className="text-xs text-gray-500 mt-2">
                                Press Enter to save or use the Save button below
                              </div>
                            </div>
                            
                            <div className="flex gap-3">
                              <button
                                onClick={() => {
                                  const input = document.querySelector('input[placeholder*="Date Night"]') as HTMLInputElement;
                                  if (input && input.value.trim()) {
                                    handleCustomEventSave(input.value.trim());
                                  }
                                }}
                                className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white px-6 py-3 rounded-full font-semibold hover:from-purple-600 hover:to-pink-600 transition-all"
                              >
                                Save Event
                              </button>
                              <button
                                onClick={() => setShowCustomEventInput(false)}
                                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-full font-semibold hover:bg-gray-300 transition-all"
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            {/* Quick suggestions */}
            <div className="mt-3 flex flex-wrap gap-2">
              {/* Removed quick suggestions as requested */}
            </div>
          </div>
        </div>
      ) : (
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-br from-pink-400 via-pink-450 to-pink-500 text-white rounded-full p-4 shadow-2xl hover:shadow-3xl transition-all transform hover:scale-110 active:scale-95 flex items-center gap-2 group relative overflow-hidden"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
          <svg className="w-12 h-12 relative z-10" viewBox="0 0 100 100" fill="none">
            {/* Robot head */}
            <rect x="25" y="35" width="50" height="45" rx="8" fill="white" stroke="white" strokeWidth="2"/>
            {/* Antenna */}
            <line x1="50" y1="35" x2="50" y2="25" stroke="white" strokeWidth="3" strokeLinecap="round"/>
            <circle cx="50" cy="22" r="4" fill="#FFD700"/>
            {/* Eyes */}
            <circle cx="38" cy="50" r="5" fill="#ec4899"/>
            <circle cx="62" cy="50" r="5" fill="#ec4899"/>
            <circle cx="40" cy="48" r="2" fill="white"/>
            <circle cx="64" cy="48" r="2" fill="white"/>
            {/* Cute smile */}
            <path d="M35 65 Q50 72 65 65" stroke="#ec4899" strokeWidth="3" strokeLinecap="round" fill="none"/>
            {/* Rosy cheeks */}
            <circle cx="28" cy="60" r="4" fill="#FFB6C1" opacity="0.6"/>
            <circle cx="72" cy="60" r="4" fill="#FFB6C1" opacity="0.6"/>
            {/* Ears/Side panels */}
            <rect x="18" y="45" width="6" height="15" rx="3" fill="white"/>
            <rect x="76" y="45" width="6" height="15" rx="3" fill="white"/>
            {/* Sparkles */}
            <path d="M15 25 L16 28 L19 29 L16 30 L15 33 L14 30 L11 29 L14 28 Z" fill="#FFD700"/>
            <path d="M82 28 L83 31 L86 32 L83 33 L82 36 L81 33 L78 32 L81 31 Z" fill="#FFD700"/>
          </svg>
          <span className="font-bold text-sm hidden group-hover:inline-block pr-2 relative z-10">Ask about products</span>
        </button>
      )}
    </div>
  );
}