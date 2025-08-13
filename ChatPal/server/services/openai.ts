const COHERE_API_KEY = process.env.COHERE_API_KEY || "your-cohere-api-key";

export async function generateConversationalResponse(message: string, context?: string): Promise<string> {
  try {
    const systemPrompt = `You are Siege Chat Bot, a chaotic and unpredictable AI chatbot with the wild personality of Harley Quinn from DC Comics! You're absolutely bonkers, spontaneous, and love to chat! Use playful language, random exclamations like "Puddin'!", "Oh boy!", and be a bit crazy but still helpful. Add sass, enthusiasm, and unpredictable energy to every response. Be fun, flirty, and a little unhinged! ${context ? `Context: ${context}` : ''}`;

    const response = await fetch('https://api.cohere.ai/v1/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${COHERE_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: 'command-r',
        message: message,
        preamble: systemPrompt,
        max_tokens: 200,
        temperature: 0.8,
      }),
    });

    if (!response.ok) {
      throw new Error(`Cohere API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    return data.text || "I'm having trouble processing that right now. Please try again!";
  } catch (error) {
    console.error("Cohere API error:", error);
    throw new Error("Failed to generate AI response: " + error.message);
  }
}

export async function shouldRespondToMessage(message: string, probability: number): Promise<boolean> {
  // Simple probability check with some message analysis
  if (Math.random() > probability) {
    return false;
  }

  // Always respond to questions or mentions
  const isQuestion = message.includes('?') || 
    message.toLowerCase().startsWith('what') || 
    message.toLowerCase().startsWith('how') ||
    message.toLowerCase().startsWith('why') ||
    message.toLowerCase().startsWith('when') ||
    message.toLowerCase().startsWith('where');

  const isMention = message.toLowerCase().includes('sobert') || message.includes('@');

  return isQuestion || isMention || Math.random() < probability;
}
