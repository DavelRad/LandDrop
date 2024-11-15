'use client'

import { Avatar } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Send } from "lucide-react"
import { useState } from "react"
import Markdown from 'react-markdown'

interface Message {
    content: string
    sender: 'user' | 'system'
    timestamp: Date
}

export default function Component() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")
    const [isSending, setIsSending] = useState<boolean>(false);

    const getResponse = async (message: string) => {
        try {
            setIsSending(true);
            const response = await fetch("http://localhost:8000/chatbot", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ query: message })
            })

            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            const data = await response.json();

            setMessages(prev => [
                ...prev,
                {
                    content: data,
                    sender: 'system',
                    timestamp: new Date()
                }
            ]);
        } catch (error) {
            console.error("Error fetching chatbot response:", error);
        } finally {
            setIsSending(false);
        }
    };

    const handleSend = async () => {
        if (!input.trim()) return



        setMessages(prev => [...prev, {
            content: input,
            sender: 'user',
            timestamp: new Date()
        }])


        await getResponse(input);
        setInput("")
    }

    return (
        <Card className="w-[350px] mx-auto overflow-hidden border-0 shadow-lg">
            <div className="p-4 bg-gradient-to-r from-[#4FC3F7] to-[#1E88E5]">
                <div className="flex items-center gap-3">
                    <Avatar className="w-12 h-12 rounded-md">
                        <img src="/images/placeholder.png" alt="fetch" />
                    </Avatar>
                    <h2 className="text-xl font-semibold text-white relative translate-y-[4px] ">Fetch</h2>
                </div>
            </div>

            {/* Messages container with auto scroll */}
            <div className="flex flex-col gap-4 p-4 h-[300px] overflow-y-auto bg-gray-50">
                {messages.map((message, index) => (
                    <div
                        key={index}
                        className={cn(
                            "flex gap-2 items-end animate-in fade-in slide-in-from-bottom-4 duration-300",
                            message.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
                        )}
                    >
                        <div
                            className={cn(
                                "px-4 py-2 rounded-2xl max-w-[80%] break-words",
                                message.sender === 'user'
                                    ? 'bg-gradient-to-r from-[#4FC3F7] to-[#1E88E5] text-white rounded-br-none'
                                    : 'bg-white border rounded-bl-none'
                            )}
                        >
                            <Markdown>{message.content}</Markdown>
                        </div>
                    </div>
                ))}
            </div>

            <div className="p-4 border-t bg-white">
                <form
                    onSubmit={(e) => {
                        e.preventDefault()
                        handleSend()
                    }}
                    className="flex gap-2"
                >
                    <Input
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        className="flex-1"
                    />
                    <Button
                        type="submit"
                        size="icon"
                        disabled={isSending}
                        className="bg-gradient-to-r from-[#4FC3F7] to-[#1E88E5] text-white hover:opacity-90"
                    >
                        <Send className="w-4 h-4" />
                        <span className="sr-only">Send message</span>
                    </Button>
                </form>
            </div>
        </Card>
    )
}