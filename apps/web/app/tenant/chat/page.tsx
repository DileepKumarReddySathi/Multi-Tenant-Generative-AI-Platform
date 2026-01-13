"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { Send, Bot, User } from "lucide-react";
import { cn } from "@/lib/utils";

export default function ChatPage() {
    const [messages, setMessages] = useState([
        { role: "assistant", content: "Hello! I'm your AI assistant. How can I help you with your documents today?" }
    ]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSend = async () => {
        if (!input.trim()) return;

        // Optimistic update
        const userMsg = { role: "user", content: input };
        setMessages(prev => [...prev, userMsg]);
        setInput("");
        setLoading(true);

        // Mock API call to RAG Service
        setTimeout(() => {
            setMessages(prev => [...prev, {
                role: "assistant",
                content: "This is a simulated RAG response. In a real deployment, I would query the Vector DB and retrieve relevant context to answer your question: '" + userMsg.content + "'"
            }]);
            setLoading(false);
        }, 1000);
    };

    return (
        <div className="flex flex-col h-[calc(100vh-8rem)]">
            <Card className="flex-1 p-4 mb-4 overflow-auto space-y-4">
                {messages.map((msg, i) => (
                    <div key={i} className={cn("flex gap-3", msg.role === "user" ? "flex-row-reverse" : "")}>
                        <div className={cn("w-8 h-8 rounded-full flex items-center justify-center shrink-0", msg.role === "assistant" ? "bg-primary text-primary-foreground" : "bg-muted")}>
                            {msg.role === "assistant" ? <Bot className="h-4 w-4" /> : <User className="h-4 w-4" />}
                        </div>
                        <div className={cn("rounded-lg px-4 py-2 max-w-[80%] text-sm", msg.role === "assistant" ? "bg-muted" : "bg-primary text-primary-foreground")}>
                            {msg.content}
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex gap-3">
                        <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center shrink-0 animate-pulse">
                            <Bot className="h-4 w-4" />
                        </div>
                        <div className="bg-muted rounded-lg px-4 py-2 text-sm text-muted-foreground">Thinking...</div>
                    </div>
                )}
            </Card>

            <div className="flex gap-2">
                <Input
                    placeholder="Ask a question about your documents..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />
                <Button onClick={handleSend} disabled={loading}>
                    <Send className="h-4 w-4" />
                </Button>
            </div>
        </div>
    );
}
