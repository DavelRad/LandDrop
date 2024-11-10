'use client'

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Skeleton } from "@/components/ui/skeleton" // Assuming you have a Skeleton component

export default function SidebarSkeleton() {
    return (
        <Card className="w-96 h-screen overflow-hidden rounded-r-xl border-black shadow-xl">
            <CardHeader className="bg-gradient-to-r from-blue-500 to-green-500 text-white">
                <CardTitle className="text-2xl font-bold">
                    <Skeleton className="h-6 w-1/2 bg-gray-300 rounded" />
                </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
                <Tabs defaultValue="details" className="w-full">
                    <TabsList className="grid w-full grid-cols-3">
                        <TabsTrigger value="details"><Skeleton className="h-4 w-full bg-gray-200" /></TabsTrigger>
                        <TabsTrigger value="correlation"><Skeleton className="h-4 w-full bg-gray-200" /></TabsTrigger>
                        <TabsTrigger value="chat"><Skeleton className="h-4 w-full bg-gray-200" /></TabsTrigger>
                    </TabsList>

                    {/* Details Tab Skeleton */}
                    <TabsContent value="details">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <Skeleton className="h-6 w-3/4 bg-gray-300 rounded" />
                                <div className="grid grid-cols-2 gap-4">
                                    <Skeleton className="h-20 bg-gray-200 rounded" />
                                    <Skeleton className="h-20 bg-gray-200 rounded" />
                                    <Skeleton className="h-20 bg-gray-200 rounded" />
                                    <Skeleton className="h-20 bg-gray-200 rounded" />
                                </div>

                                <div>
                                    <Skeleton className="h-6 w-1/2 bg-gray-300 rounded mb-4" />
                                    <Skeleton className="h-48 w-full bg-gray-200 rounded" />
                                </div>
                            </div>
                        </ScrollArea>
                    </TabsContent>

                    {/* Correlation Tab Skeleton */}
                    <TabsContent value="correlation">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <Skeleton className="h-6 w-3/4 bg-gray-300 rounded" />
                                <Skeleton className="h-48 w-full bg-gray-200 rounded" />
                            </div>
                        </ScrollArea>
                    </TabsContent>

                    {/* Chat Tab Skeleton */}
                    <TabsContent value="chat">
                        <ScrollArea className="h-[calc(100vh-250px)]">
                            <Skeleton className="h-48 w-full bg-gray-200 rounded" />
                        </ScrollArea>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    )
}
