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
    const [location, setLocation] = useState<Location | null>(null)
    const [soilData, setSoilData] = useState<SoilData | null>(null)
    const [loadingstatus, setIsloading] = useState(false)

    // Fetch the soil data from backend
    const fetchSoilData = async (loc: Location) => {
        try {
            setIsloading(true) // Start loading
            setSoilData(null) // Reset previous data

            const response = await fetch('http://localhost:8000/endpoint', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    lat: loc.lat,
                    lon: loc.lon,
                }),
            })

            if (!response.ok) {
                throw new Error('Failed to fetch soil data')
            }

            const data = await response.json()

            const recentSoilData: SoilData = {
                valid_date: data.soil_data[0].valid_date,
                bulk_soil_density: data.soil_data[0].bulk_soil_density,
                temp_2m_avg: data.soil_data[0].temp_2m_avg,
                evapotranspiration: data.soil_data[0].evapotranspiration,
                wind_10m_spd_avg: data.soil_data[0].wind_10m_spd_avg,
                precip: data.soil_data[0].precip,
                v_soilm_0_10cm: data.soil_data[0].v_soilm_0_10cm,
                v_soilm_10_40cm: data.soil_data[0].v_soilm_10_40cm,
                v_soilm_40_100cm: data.soil_data[0].v_soilm_40_100cm,
                v_soilm_100_200cm: data.soil_data[0].v_soilm_100_200cm,
                dlwrf_avg: 0,
                dlwrf_max: 0,
                dlwrf_net: 0,
                dswrf_avg: 0,
                dswrf_max: 0,
                dswrf_net: 0,
                pres_avg: 0,
                skin_temp_avg: 0,
                skin_temp_max: 0,
                skin_temp_min: 0,
                soilm_0_10cm: 0,
                soilm_100_200cm: 0,
                soilm_10_40cm: 0,
                soilm_40_100cm: 0,
                soilt_0_10cm: 0,
                soilt_100_200cm: 0,
                soilt_10_40cm: 0,
                soilt_40_100cm: 0,
                specific_humidity: 0
            }

            setSoilData(recentSoilData) // Set fetched data
        } catch (error) {
            console.error(error)
        } finally {
            setIsloading(false) // Stop loading
        }
    }

    useEffect(() => {
        if (map.current || !mapContainer.current) return

        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: style,
            center: [-74.5, 40],
            zoom: 9,
        })

        map.current.on('click', async (e) => {
            const clickedLocation = {
                lat: e.lngLat.lat,
                lon: e.lngLat.lng
            }
            console.log("Clicked location:", clickedLocation)
            setLocation(clickedLocation)

            await fetchSoilData(clickedLocation) // Fetch data for clicked location
        })

        return () => map.current?.remove()
    }, [])

    return (
        <div className="relative h-screen">
            <AnimatePresence>
                {loadingstatus && (
                    <motion.div
                        key="loading"
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute top-0 left-0 right-0 z-10"
                    >
                        <LoadSideBar />
                    </motion.div>
                )}
                {!loadingstatus && location && soilData && (
                    <motion.div
                        key="sidebar"
                        initial={{ opacity: 0, x: -100 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -100 }}
                        transition={{ duration: 0.3 }}
                        className="absolute top-0 left-0 right-0 z-10 m-4"
                    >
                        <Sidebar theLocation={location} soilData={soilData} />
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
                        <ChatComponent />
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}
