'use client'

import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import Sidebar from '@/components/sidebar'
import ChatComponent from '@/components/ChatComponent'

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || ""
const style = process.env.NEXT_PUBLIC_MAPBOX_STYLE || ""

export type Location = {
    lat: number
    lon: number
}

export type SoilData = {
    date: string
    bulk_soil_density: number
    skin_temp_max: number
    skin_temp_avg: number
    skin_temp_min: number
    temp_2m_avg: number
    precip: number
    specific_humidity: number
    evapotranspiration: number
    pres_avg: number
    wind_10m_spd_avg: number
    dlwrf_avg: number
    dlwrf_max: number
    dswrf_avg: number
    dswrf_max: number
    dswrf_net: number
    dlwrf_net: number
    soilm_0_10cm: number
    soilm_10_40cm: number
    soilm_40_100cm: number
    soilm_100_200cm: number
    v_soilm_0_10cm: number
    v_soilm_10_40cm: number
    v_soilm_40_100cm: number
    v_soilm_100_200cm: number
    soilt_0_10cm: number
    soilt_10_40cm: number
    soilt_40_100cm: number
    soilt_100_200cm: number
}

export default function Map() {
    const mapContainer = useRef<HTMLDivElement>(null)
    const map = useRef<mapboxgl.Map | null>(null)
    const markerRef = useRef<mapboxgl.Marker | null>(null)
    const [location, setLocation] = useState<Location | null>(null)
    const [soilData, setSoilData] = useState<SoilData | null>(null)

    const fetchSoilData = async (): Promise<SoilData> => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    date: "2023-05-15",
                    bulk_soil_density: 1390,
                    skin_temp_max: 34.5,
                    skin_temp_avg: 26.5,
                    skin_temp_min: 13.5,
                    temp_2m_avg: 22.1,
                    precip: 0,
                    specific_humidity: 0.00329,
                    evapotranspiration: 0.925,
                    pres_avg: 918.072,
                    wind_10m_spd_avg: 2.877,
                    dlwrf_avg: 350.53,
                    dlwrf_max: 600.53,
                    dswrf_avg: 473.555,
                    dswrf_max: 870.555,
                    dswrf_net: -23.408,
                    dlwrf_net: 416.075,
                    soilm_0_10cm: 14.804,
                    soilm_10_40cm: 53.016,
                    soilm_40_100cm: 112.557,
                    soilm_100_200cm: 200.732,
                    v_soilm_0_10cm: 0.148,
                    v_soilm_10_40cm: 0.177,
                    v_soilm_40_100cm: 0.188,
                    v_soilm_100_200cm: 0.201,
                    soilt_0_10cm: 19.9,
                    soilt_10_40cm: 15,
                    soilt_40_100cm: 14.2,
                    soilt_100_200cm: 14.6
                })
            }, 500)
        })
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
            setLocation(clickedLocation)

            const fetchedSoilData = await fetchSoilData()
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
                {location && soilData && (
                    <motion.div
                        key="sidebar"
                        initial={{ opacity: 0, y: -50 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -50 }}
                        transition={{ duration: 0.5 }}
                        className="absolute top-0 left-0 right-0 z-10 m-4 max-w-48"
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
