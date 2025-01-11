import re
import csv
import io
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/parse', methods=['POST'])
def validate_ingredients():
    data = request.json

    if 'string' not in data or not data['string']:
        return jsonify({"error": "Ingredients Must Not Be Empty"}), 400

    ingredients = data['string']

    # Sanitize ingredients string
    sanitized_ingredients = re.sub(r'[^\x20-\x7E]', '', ingredients)  # Remove non-ASCII characters

    print(f"Received string: {sanitized_ingredients}")

    # Process data and generate CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Ingredient'])
    writer.writerow([sanitized_ingredients])

    # Your additional logic for handling the CSV output...

    return jsonify({"message": "Ingredients processed successfully!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
