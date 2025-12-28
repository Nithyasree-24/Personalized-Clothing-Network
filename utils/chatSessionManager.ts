/**
 * Chat Session Manager for FashionPulse
 * Handles chat persistence and logout integration
 */

export class ChatSessionManager {
  private static instance: ChatSessionManager;
  
  private constructor() {}
  
  public static getInstance(): ChatSessionManager {
    if (!ChatSessionManager.instance) {
      ChatSessionManager.instance = new ChatSessionManager();
    }
    return ChatSessionManager.instance;
  }
  
  /**
   * Clear chat session for current user
   * Call this when user logs out
   */
  public clearChatSession(): void {
    try {
      const userId = localStorage.getItem('user_id') || 'guest';
      const chatKey = `fashionpulse_chat_${userId}`;
      
      // Remove chat data from localStorage
      localStorage.removeItem(chatKey);
      
      // Dispatch logout event to notify chat component
      window.dispatchEvent(new CustomEvent('fashionpulse-logout', {
        detail: { userId, timestamp: new Date().toISOString() }
      }));
      
      // Also call global function if available
      if ((window as any).clearFashionPulseChat) {
        (window as any).clearFashionPulseChat();
      }
      
      console.log('Chat session cleared for user:', userId);
    } catch (error) {
      console.error('Error clearing chat session:', error);
    }
  }
  
  /**
   * Get chat session info for current user
   */
  public getChatSessionInfo(): { hasSession: boolean; userId: string; lastUpdated?: string } {
    try {
      const userId = localStorage.getItem('user_id') || 'guest';
      const chatKey = `fashionpulse_chat_${userId}`;
      const savedChatState = localStorage.getItem(chatKey);
      
      if (savedChatState) {
        const chatData = JSON.parse(savedChatState);
        return {
          hasSession: true,
          userId,
          lastUpdated: chatData.lastUpdated
        };
      }
      
      return { hasSession: false, userId };
    } catch (error) {
      console.error('Error getting chat session info:', error);
      return { hasSession: false, userId: 'unknown' };
    }
  }
  
  /**
   * Initialize chat session for new user
   * Call this when user logs in
   */
  public initializeChatSession(userId: string): void {
    try {
      // Store user ID for chat persistence
      localStorage.setItem('user_id', userId);
      
      console.log('Chat session initialized for user:', userId);
    } catch (error) {
      console.error('Error initializing chat session:', error);
    }
  }
  
  /**
   * Check if chat should persist (user is logged in)
   */
  public shouldPersistChat(): boolean {
    const userId = localStorage.getItem('user_id');
    const token = localStorage.getItem('token') || localStorage.getItem('auth_token');
    
    return !!(userId && token);
  }
}

// Export singleton instance
export const chatSessionManager = ChatSessionManager.getInstance();

// Global functions for easy integration
(window as any).FashionPulseChatManager = {
  clearSession: () => chatSessionManager.clearChatSession(),
  initSession: (userId: string) => chatSessionManager.initializeChatSession(userId),
  getSessionInfo: () => chatSessionManager.getChatSessionInfo(),
  shouldPersist: () => chatSessionManager.shouldPersistChat()
};