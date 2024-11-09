"use client";
import { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "mapbox-gl/dist/mapbox-gl.css";

mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN || "";
const style = process.env.NEXT_PUBLIC_MAPBOX_STYLE || "";

export default function Map() {
    const mapContainer = useRef(null);
    const map = useRef<mapboxgl.Map | null>(null);


    useEffect(() => {
        if (map.current) return;

        if (mapContainer.current) {
            map.current = new mapboxgl.Map({
                container: mapContainer.current,
                style: style,
                center: [-74.5, 40],
                zoom: 9,
            });
        }
    }, []);

    return <div ref={mapContainer} style={{ width: "100%", height: "100vh" }} />;
}
