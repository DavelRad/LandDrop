'use client'
import dynamic from 'next/dynamic';

const Map = dynamic(() => import('../../components/Map'), { ssr: false });

export default function Page() {
    return (
        <div >
            <h1>Mapbox in Next.js</h1>
            <Map />
        </div>
    );
}
