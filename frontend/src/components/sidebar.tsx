'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Layers, Thermometer, Droplets, Wind } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { SoilData, Location } from './Map'

type SidebarProps = {
    theLocation?: Location
    soilData?: SoilData
}

export default function Sidebar({ theLocation, soilData }: SidebarProps) {
    if (!theLocation || !soilData) {
        return null
    }

    return (
        <Card className="w-96 h-full overflow-hidden rounded-r-xl border-black shadow-xl ">
            <CardHeader className="bg-gradient-to-r from-[#4FC3F7] to-[#1E88E5] text-white">
                <CardTitle className="text-2xl font-bold">Soil Analysis</CardTitle>
                <CardDescription className="text-gray-100">
                    {`Lat: ${theLocation.lat.toFixed(4)}, Lon: ${theLocation.lon.toFixed(4)}`}
                </CardDescription>
            </CardHeader>
            <CardContent className="p-0">
                <Tabs defaultValue="details" className="w-full">
                    <TabsList className="grid w-full grid-cols-3">
                        <TabsTrigger value="details">Details</TabsTrigger>
                        <TabsTrigger value="correlation">Correlation</TabsTrigger>
                        <TabsTrigger value="chat">Chat</TabsTrigger>
                    </TabsList>

                    {/* Details Tab */}
                    <TabsContent value="details">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <div className="flex justify-between items-center">
                                    <h3 className="text-lg font-semibold">Date: {soilData.date}</h3>
                                    <Badge variant="outline" className="text-sm">
                                        {soilData.precip === 0 ? 'No Rain' : `${soilData.precip} mm Rain`}
                                    </Badge>
                                </div>
                                <div className="grid grid-cols-2 gap-4">
                                    <Card className="p-4 flex items-center space-x-2">
                                        <Layers className="text-blue-500" />
                                        <div>
                                            <p className="text-sm text-gray-500">Soil Density</p>
                                            <p className="font-semibold">{soilData.bulk_soil_density} kg/m³</p>
                                        </div>
                                    </Card>
                                    <Card className="p-4 flex items-center space-x-2">
                                        <Thermometer className="text-red-500" />
                                        <div>
                                            <p className="text-sm text-gray-500">Avg. Temp (2m)</p>
                                            <p className="font-semibold">{soilData.temp_2m_avg}°C</p>
                                        </div>
                                    </Card>
                                    <Card className="p-4 flex items-center space-x-2">
                                        <Droplets className="text-blue-500" />
                                        <div>
                                            <p className="text-sm text-gray-500">Evapotranspiration</p>
                                            <p className="font-semibold">{soilData.evapotranspiration} mm</p>
                                        </div>
                                    </Card>
                                    <Card className="p-4 flex items-center space-x-2">
                                        <Wind className="text-gray-500" />
                                        <div>
                                            <p className="text-sm text-gray-500">Wind Speed</p>
                                            <p className="font-semibold">{soilData.wind_10m_spd_avg} m/s</p>
                                        </div>
                                    </Card>
                                </div>

                                <div>
                                    <h4 className="font-semibold mb-4">Soil Moisture Profile</h4>
                                    <ResponsiveContainer width="100%" height={200}>
                                        <LineChart data={[
                                            { depth: '0-10cm', moisture: soilData.v_soilm_0_10cm },
                                            { depth: '10-40cm', moisture: soilData.v_soilm_10_40cm },
                                            { depth: '40-100cm', moisture: soilData.v_soilm_40_100cm },
                                            { depth: '100-200cm', moisture: soilData.v_soilm_100_200cm },
                                        ]}>
                                            <CartesianGrid strokeDasharray="3 3" />
                                            <XAxis dataKey="depth" />
                                            <YAxis />
                                            <Tooltip />
                                            <Legend />
                                            <Line type="monotone" dataKey="moisture" stroke="#3b82f6" strokeWidth={2} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </ScrollArea>
                    </TabsContent>

                    {/* Correlation Tab */}
                    <TabsContent value="correlation">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <h3 className="text-lg font-semibold">Correlation Graphs</h3>
                            </div>
                        </ScrollArea>
                    </TabsContent>

                    {/* Chat Tab */}
                    <TabsContent value="chat">
                        <ScrollArea className="h-[calc(100vh-250px)]">
                            {/* Placeholder for chat content */}
                        </ScrollArea>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card>
    )
}
