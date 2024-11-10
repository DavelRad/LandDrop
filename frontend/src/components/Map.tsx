'use client'

import { useState, useEffect, useRef } from 'react'

import { motion, AnimatePresence } from 'framer-motion'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import Sidebar from '@/components/sidebar'
import ChatComponent from '@/components/ChatComponent'
import LoadSideBar from '@/components/LoadSideBar'


mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || ""
const style = process.env.NEXT_PUBLIC_MAPBOX_STYLE || ""

export type Location = {
    lat: number
    lon: number
}

export type SoilData = {
    bulk_soil_density: number
    dlwrf_avg: number
    dlwrf_max: number
    dlwrf_net: number
    dswrf_avg: number
    dswrf_max: number
    dswrf_net: number
    evapotranspiration: number
    precip: number
    pres_avg: number
    skin_temp_avg: number
    skin_temp_max: number
    skin_temp_min: number
    soilm_0_10cm: number
    soilm_100_200cm: number
    soilm_10_40cm: number
    soilm_40_100cm: number
    soilt_0_10cm: number
    soilt_100_200cm: number
    soilt_10_40cm: number
    soilt_40_100cm: number
    specific_humidity: number
    temp_2m_avg: number
    v_soilm_0_10cm: number
    v_soilm_100_200cm: number
    v_soilm_10_40cm: number
    v_soilm_40_100cm: number
    valid_date: string
    wind_10m_spd_avg: number
}

export default function Map() {
    const mapContainer = useRef<HTMLDivElement>(null)
    const map = useRef<mapboxgl.Map | null>(null)
    const markerRef = useRef<mapboxgl.Marker | null>(null)
    const [location, setLocation] = useState<Location | null>(null)
    const [soilData, setSoilData] = useState<SoilData | null>(null)
    const [loadingStatus, setLoadingStatus] = useState<boolean>(false);
    const [selectedDate, setSelectedDate] = useState<string>('')
    const [dates, setDates] = useState<string[]>([])
    const [soilDataArray, setSoilDataArray] = useState<SoilData[]>([]);
    const [checkState, setCheckState] = useState<String>('');
    const [droughtData, setDroughtData] = useState<number[]>([]);


    const fetchSoilData = async (lat: number, lon: number): Promise<SoilData | null> => {
        try {
            setLoadingStatus(true);
            setSelectedDate('');
            const response = await fetch(`http://localhost:8000/endpoint`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ lat, lon }),
            })

            if (!response.ok) {
                console.error('Failed to fetch soil data')
                return null
            }

            const data = await response.json()
            // console.log("Data");
            setDates(data.soil_data.map((soilData: SoilData) => soilData.valid_date))
            setSoilDataArray(data.soil_data);
            setDroughtData(data["drought_percentage"]);

            setCheckState(data['drought_percentage']);
            return !selectedDate ? data.soil_data[data.soil_data.length - 1] : data.soil_data.find((soilData: SoilData) => soilData.valid_date === selectedDate)
        } catch (error) {
            console.error('Error fetching soil data:', error)
            return null
        } finally {
            setLoadingStatus(false);
        }
    }

    useEffect(() => {
        console.log("State here wooo whoooo ", checkState);
    }, [checkState])

    useEffect(() => {
        if (soilDataArray && soilDataArray.length > 0) {
            const selectedSoilData = soilDataArray.find((data: SoilData) => data.valid_date === selectedDate);
            setSoilData(selectedSoilData || soilDataArray[soilDataArray.length - 1]);
            console.log(selectedDate);
        }
    }, [selectedDate, soilData]);

    useEffect(() => {
        if (map.current || !mapContainer.current) return


        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            // style: style,
            center: [-74.5, 40],
            zoom: 9,
        })

        map.current.on('click', async (e) => {
            const clickedLocation = {
                lat: e.lngLat.lat,
                lon: e.lngLat.lng
            }
            setLocation(clickedLocation)

            const fetchedSoilData = await fetchSoilData(clickedLocation.lat, clickedLocation.lon)
            setSoilData(fetchedSoilData)

            if (markerRef.current) {
                markerRef.current.remove()
            }


            markerRef.current = new mapboxgl.Marker({ color: 'red' })
                .setLngLat([clickedLocation.lon, clickedLocation.lat])
                .addTo(map.current!)
        })

        return () => {
            map.current?.remove()
        }
    }, [])

    return (
        <div className="relative h-screen">
            <AnimatePresence>
                {loadingStatus && (
                    <motion.div
                        key="loading"
                        initial={{ opacity: 0, y: -50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute top-0 left-0 right-0 z-10 m-4 max-w-48"
                    >
                        <LoadSideBar />
                    </motion.div>
                )}
                {!loadingStatus && location && soilData && (
                    <motion.div
                        key="sidebar"
                        initial={{ opacity: 0, y: -50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute top-0 left-0 right-0 z-10 m-4 max-w-48"
                    >
                        <Sidebar theLocation={location} soilData={soilData} dates={dates} setDateState={setSelectedDate} soilDataArray={soilDataArray} droughtData={droughtData} />
                    </motion.div>
                )}
            </AnimatePresence>
            <div className="w-full h-full relative">
                <div ref={mapContainer} className="w-full h-full" />
            </div>
            <AnimatePresence>
                {location && soilData && (
                    <motion.div
                        key="chat"
                        initial={{ opacity: 0, y: 50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: 50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute bottom-2 right-4 z-20"
                    >
                        {!loadingStatus &&
                            <ChatComponent />
                        }
                    </motion.div>
                )}
            </AnimatePresence>
        </div>

    )
}
