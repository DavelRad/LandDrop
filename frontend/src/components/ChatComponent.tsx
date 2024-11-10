'use client'

import { Avatar } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Send } from "lucide-react"
import { useState } from "react"

interface Message {
    content: string
    sender: 'user' | 'farmer'
    timestamp: Date
}

export default function Component() {
    const [messages, setMessages] = useState<Message[]>([])
    const [input, setInput] = useState("")

    const handleSend = () => {
        if (!input.trim()) return

        setMessages(prev => [...prev, {
            content: input,
            sender: 'user',
            timestamp: new Date()
        }])
        setInput("")
    }

    return (
        <Card className="w-full max-w-lg mx-auto overflow-hidden border-0 shadow-lg">
            <div className="p-4 bg-gradient-to-r from-[#4FC3F7] to-[#1E88E5]">
                <div className="flex items-center gap-3">
                    <Avatar className="w-8 h-8">
                        <img src="/images/placeholder.png" alt="Farmer Brady" />
                    </Avatar>
                    <h2 className="text-lg font-semibold text-white">Chat with Farmer Brady</h2>
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
                            {message.content}
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