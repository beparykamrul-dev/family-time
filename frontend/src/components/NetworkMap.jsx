import React from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix default icon issue
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
})

function NetworkMap({ devices = [], center = [23.8103, 90.4125], zoom = 12 }) {
  return (
    <div className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow border border-gray-200 dark:border-gray-700">
      <h3 className="text-lg font-semibold mb-2 text-gray-900 dark:text-white">Network Map</h3>
      <div style={{ width: '100%', height: 360 }} className="rounded-md overflow-hidden">
        <MapContainer center={center} zoom={zoom} style={{ height: '100%', width: '100%' }}>
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          {devices.map((d) => (
            <Marker key={d.id} position={[d.latitude, d.longitude]}>
              <Popup>
                <div className="text-sm">
                  <strong>{d.name}</strong>
                  <div>{d.type}</div>
                  <div>Status: {d.status}</div>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  )
}

export default NetworkMap
