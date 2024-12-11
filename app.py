from flask import Flask, request, jsonify
from scrape import scrape_publication  # Importa la función de scrapeo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data['url']
        print(f"Procesando URL: {url}")  # Para depuración
        result = scrape_publication(url)
        if result:
            return jsonify(result)
        return jsonify({"error": "No se pudo extraer la información.", "url": url})
    except Exception as e:
        return jsonify({"error": str(e), "url": url})

if __name__ == "__main__":
    app.run(debug=True, port=5000)