
odoo.define('farmaprecio.store_map', function (require) {
    'use strict';
    let map;
    $(document).ready(function () {
        console.log("Script de Google Maps cargado.");
        async function initMap() {
            console.log("Inicializando el mapa...");
            try {
                const { Map } = await google.maps.importLibrary("maps");
                map = new Map(document.getElementById("map"), {
                    zoom: 10,
                    center: { lat: 14.6349, lng: -90.5069 },
                });
                console.log("Mapa inicializado correctamente.");

                // Datos de prueba o cargados dinámicamente
                const stores = window.storeData || [];
                console.log("Datos de tiendas:", stores);

                // Agregar marcadores
                stores.forEach((store) => {
                    if (store.latitude && store.longitude) {
                        const marker = new google.maps.Marker({
                            position: { lat: parseFloat(store.latitude), lng: parseFloat(store.longitude) },
                            map: map,
                            title: store.name,
                        });

                        // Ventana de información
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
                    }
                });
            } catch (error) {
                console.error("Error inicializando el mapa:", error);
            }
        }
        window.initMap = initMap;
        
        if (document.getElementById("map")) {
            initMap();
        } else {
            console.error("El contenedor del mapa no está disponible.");
        }
    });
});