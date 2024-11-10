'use client'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Layers, Thermometer, Droplets, Wind } from 'lucide-react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { SoilData, Location } from './Map'
import {
    Select,
    SelectLabel,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"


type SidebarProps = {
    theLocation?: Location
    soilData?: SoilData,
    soilDataArray: SoilData[],
    dates?: string[]
    setDateState: any,
    droughtData: number[],
    landDegradation: number[]
}

export default function Sidebar({ theLocation, soilData, dates, setDateState, soilDataArray, droughtData, landDegradation }: SidebarProps) {
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
                        <TabsTrigger value="details">Land Details</TabsTrigger>
                        <TabsTrigger value="social">Social Details</TabsTrigger>
                        <TabsTrigger value="correlation">Correlation</TabsTrigger>
                    </TabsList>

                    {/* Details Tab */}
                    <TabsContent value="details">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <div className="flex justify-between items-center">
                                    <h3 className="text-lg font-semibold">Date: </h3>
                                    <Select onValueChange={(v) => setDateState(v)}>
                                        <SelectTrigger className="w-[180px]">
                                            <SelectValue placeholder={dates ? dates[0] : "Choose a date"} />
                                        </SelectTrigger>
                                        <SelectContent>
                                            <SelectGroup>
                                                <SelectLabel>Date</SelectLabel>
                                                {dates?.map((date, index) => (
                                                    <SelectItem key={date} value={date}>
                                                        {index === 0 ? date : `${index} day${index > 1 ? 's' : ''} ago`}
                                                    </SelectItem>
                                                ))}
                                            </SelectGroup>
                                        </SelectContent>
                                    </Select>
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
                                <ResponsiveContainer width="100%" height={200}>
                                    <LineChart data={
                                        Array.isArray(soilDataArray) && Array.isArray(droughtData)
                                            ? soilDataArray.map((entry, index) => ({
                                                date: entry.valid_date, // x-axis value from soilDataArray's valid_date
                                                drought: droughtData[index] // y-axis value from droughtPercentages
                                            }))
                                            : []
                                    }
                                        margin={{ right: 30 }}
                                    >
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="date" />
                                        <YAxis label={{ value: "Drought %", angle: -90, position: 'middle' }} tickMargin={200} />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey="drought" stroke="#e63946" strokeWidth={4} />
                                    </LineChart>

                                </ResponsiveContainer>
                                <ResponsiveContainer height={200}>
                                    <LineChart data={
                                        Array.isArray(soilDataArray) && Array.isArray(landDegradation)
                                            ? soilDataArray.map((entry, index) => ({
                                                date: entry.valid_date, // x-axis value from soilDataArray's valid_date
                                                landDegradation: landDegradation[index] // y-axis value from droughtPercentages
                                            }))
                                            : []

                                    }
                                        margin={{ right: 30 }}
                                    >
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="date" />
                                        <YAxis label={{ value: "Degradation %", angle: -90, position: 'middle' }} tickMargin={200} />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey="landDegradation" stroke="#008000" strokeWidth={4} />
                                    </LineChart>
                                </ResponsiveContainer>
                                <ResponsiveContainer height={200}>
                                    <LineChart
                                        data={
                                            Array.isArray(droughtData) && Array.isArray(landDegradation)
                                                ? droughtData.map((drought, index) => ({
                                                    date: drought, // Assuming `drought` contains date information for x-axis consistency
                                                    landDegradation: landDegradation[index]
                                                }))
                                                : []
                                        }
                                        margin={{ right: 30 }}
                                    >
                                        <CartesianGrid strokeDasharray="3 3" />
                                        <XAxis dataKey="date" />
                                        <YAxis
                                            label={{ value: "Degradation %", angle: -90, position: 'middle' }}
                                            tickMargin={200}
                                        />
                                        <Tooltip />
                                        <Legend />
                                        <Line type="monotone" dataKey="landDegradation" stroke="#008000" strokeWidth={4} />
                                    </LineChart>
                                </ResponsiveContainer>


                            </div>
                        </ScrollArea>
                    </TabsContent>
                    <TabsContent value="social">
                        <ScrollArea className="h-[calc(100vh-200px)]">
                            <div className="p-6 space-y-6">
                                <h3 className="text-lg font-semibold">Socioeconomic Details</h3>
                            </div>
                        </ScrollArea>
                    </TabsContent>
                </Tabs>
            </CardContent>
        </Card >
    )
}
