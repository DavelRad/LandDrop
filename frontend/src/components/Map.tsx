'use client'

import { useState, useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
import Sidebar from '@/components/sidebar'

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
    const [location, setLocation] = useState<Location | null>(null)
    const [soilData, setSoilData] = useState<SoilData | null>(null)

    // Function to simulate fetching soil data
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

        // Handle map click event to set location and fetch soil data
        map.current.on('click', async (e) => {
            const clickedLocation = {
                lat: e.lngLat.lat,
                lon: e.lngLat.lng
            }
            console.log("Clicked location:", clickedLocation)
            setLocation(clickedLocation)

            // Fetch and set soil data after setting location
            const fetchedSoilData = await fetchSoilData()
            console.log("Fetched soil data:", fetchedSoilData)
            setSoilData(fetchedSoilData)
        })

        return () => {
            map.current?.remove()  // Clean up map on component unmount
        }
    }, [])

    return (
        <div className="relative h-screen">
            {location && soilData && (
                <div className="absolute top-0 left-0 right-0 z-10 m-4 max-w-48">
                    <Sidebar theLocation={location} soilData={soilData} />
                </div>
            )}
            <div className="w-full h-full relative">
                <div ref={mapContainer} className="w-full h-full" />
            </div>
        </div>

    )
}
