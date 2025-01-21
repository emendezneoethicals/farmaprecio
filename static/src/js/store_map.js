odoo.define('farmaprecio.store_map', function (require) {
    'use strict';
    let map;

    $(document).ready(function () {
        console.log("Script de Google Maps cargado.");

        async function initMap() {
            console.log("Inicializando el mapa...");
            try {
                const { Map } = await google.maps.importLibrary("maps");
                const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

                // Inicializa el mapa centrado en una ubicación predeterminada
                map = new Map(document.getElementById("map"), {
                    zoom: 10,
                    center: { lat: 14.6349, lng: -90.5069 },
                     mapId: "DEMO_MAP_ID",
                });
                console.log("Mapa inicializado correctamente.");

                // Obtiene los datos de las tiendas
                const stores = window.storeData || [];
                console.log("Datos de tiendas:", stores);

                // Crea una instancia de LatLngBounds para ajustar los límites del mapa
                const bounds = new google.maps.LatLngBounds();

                // Limpia los marcadores existentes
                let markers = [];

                // Agrega marcadores y extiende los límites
                stores.forEach((store) => {
                    if (store.latitude && store.longitude) {
                        const position = { lat: parseFloat(store.latitude), lng: parseFloat(store.longitude) };
                        const marker = new AdvancedMarkerElement({
                            position: position,
                            map: map,
                            title: store.name,
                        });

                        // Crea una ventana de información para cada marcador
                        const wazeLink = `https://www.waze.com/ul?ll=${store.latitude},${store.longitude}&navigate=yes`;
                        const infoWindow = new google.maps.InfoWindow({
                            content: `
                                <div>
                                    <h5>${store.name}</h5>
                                    <p><strong>Dirección:</strong> ${store.address}</p>
                                    <p><strong>Teléfono:</strong> ${store.phone}</p>
                                    <p><strong>Horario:</strong> ${store.opening_hours}</p>
                                    <a href="${wazeLink}" target="_blank" style="display: flex; align-items: center; text-decoration: none; color: #1a73e8;">
                                        <img src="/farmaprecio/static/src/img/waze.png" alt="Waze" style="width: 20px; height: 20px; margin-right: 5px;">
                                        Navegar con Waze
                                    </a>
                                </div>
                            `,
                        });

                        marker.addListener("click", () => {
                            infoWindow.open(map, marker);
                        });

                        markers.push(marker);

                        // Extiende los límites para incluir la posición del marcador
                        bounds.extend(position);
                    }
                });

                // Ajustar el mapa según la cantidad de marcadores
                if (markers.length === 1) {
                    // Si hay solo un marcador, centra el mapa en sus coordenadas
                    const singleMarker = markers[0];
                    map.setCenter(singleMarker.position);
                    map.setZoom(15); // Zoom ajustado para un solo marcador
                } else if (markers.length > 1) {
                    // Si hay múltiples marcadores, ajusta los límites
                    map.fitBounds(bounds);
                } else {
                    // Si no hay marcadores, centra en la ubicación predeterminada
                    map.setCenter({ lat: 14.6349, lng: -90.5069 });
                    map.setZoom(10);
                }
            } catch (error) {
                console.error("Error inicializando el mapa:", error);
            }
        }

        // Asignar la función initMap al contexto global
        window.initMap = initMap;

        // Inicializar el mapa si el contenedor está disponible
        if (document.getElementById("map")) {
            initMap();
        } else {
            console.error("El contenedor del mapa no está disponible.");
        }
    });
});
