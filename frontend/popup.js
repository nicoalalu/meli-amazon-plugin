document.getElementById('scrape-button').addEventListener('click', async () => {
    try {
        const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
        const url = tab.url;
        console.log('URL actual:', url); // Log 1
        
        if (!url.includes('mercadolibre')) {
            console.log('No es una URL de MercadoLibre'); // Log 2
            document.getElementById('result').innerHTML = 
                '<p>Esta página no es de MercadoLibre</p>';
            return;
        }

        console.log('Enviando solicitud al backend...'); // Log 3
        const response = await fetch('http://localhost:5000/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        console.log('Respuesta recibida del backend'); // Log 4
        const data = await response.json();
        console.log('Datos recibidos:', data); // Log 5
        
        const resultDiv = document.getElementById('result');
        
        if (data && !data.error) {
            resultDiv.innerHTML = `
                <p><strong>Nombre Publicación:</strong> ${data[0]}</p>
                <p><strong>Nombre Producto:</strong> ${data[1]}</p>
                <p><strong>Precio:</strong> ${data[2]}</p>
            `;
        } else {
            console.log('Error en los datos:', data.error); // Log 6
            resultDiv.innerHTML = `<p>No se pudo extraer información.</p>`;
        }
    } catch (error) {
        console.error('Error detallado:', error); // Log más detallado
        document.getElementById('result').innerHTML = 
            '<p>Error al procesar la solicitud</p>';
    }
});