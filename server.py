from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import math
import statistics

app = Flask(__name__)

### SWAGGER CONFIGURATION ###
SWAGGER_URL = "/api/docs"
API_URL = "/static/swagger.json"
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route("/factorial", methods=["GET"])
def calculate_factorial():
    """
    Calculate the factorial of a number (n!).
    ---
    parameters:
      - name: n
        in: query
        type: integer
        required: true
        description: "Positive integer to calculate factorial for"
        minimum: 0
        maximum: 100  # Per evitare numeri troppo grandi
    responses:
      200:
        description: "Factorial calculated successfully"
      400:
        description: "Invalid input (must be integer between 0 and 100)"
    """
    try:
        n = int(request.args.get("n"))
        if n < 0 or n > 100:
            return jsonify({"error": "Number must be between 0 and 100"}), 400
        
        result = math.factorial(n)
        return jsonify({"number": n, "factorial": result})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input - must be an integer"}), 400

@app.route("/harmonic_number", methods=["GET"])
def calculate_harmonic_number():
    """
    Calculate the n-th harmonic number (Hₙ = 1 + 1/2 + 1/3 + ... + 1/n).
    ---
    parameters:
      - name: n
        in: query
        type: integer
        required: true
        description: "Positive integer to calculate harmonic number for"
        minimum: 1
        maximum: 10000
    responses:
      200:
        description: "Harmonic number calculated successfully"
      400:
        description: "Invalid input (must be integer ≥ 1)"
    """
    try:
        n = int(request.args.get("n"))
        if n < 1:
            return jsonify({"error": "Number must be ≥ 1"}), 400
        
        harmonic = sum(1/i for i in range(1, n+1))
        return jsonify({"n": n, "harmonic_number": harmonic})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input - must be an integer"}), 400

@app.route("/triangular_number", methods=["GET"])
def calculate_triangular_number():
    """
    Calculate the n-th triangular number (Tₙ = n(n+1)/2).
    ---
    parameters:
      - name: n
        in: query
        type: integer
        required: true
        description: "Positive integer to calculate triangular number for"
        minimum: 0
        maximum: 1000000
    responses:
      200:
        description: "Triangular number calculated successfully"
      400:
        description: "Invalid input (must be integer ≥ 0)"
    """
    try:
        n = int(request.args.get("n"))
        if n < 0:
            return jsonify({"error": "Number must be ≥ 0"}), 400
        
        triangular = n * (n + 1) // 2
        return jsonify({"n": n, "triangular_number": triangular})
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid input - must be an integer"}), 400


@app.route('/statistical_metrics', methods=['GET'])
def statistical_metrics():
    try:
        # Ottieni tutti i parametri numerici dalla query string
        numbers = [float(v) for k, v in request.args.items() if k.startswith('num')]
        
        if len(numbers) < 2:
            return jsonify({'error': 'Inserire almeno 2 valori numerici (num1, num2, ...)'}), 400
        
        # Calcoli statistici di base
        results = {
            'input_numbers': numbers,
            'count': len(numbers),
            'sum': sum(numbers),
            'mean': statistics.mean(numbers),
            'median': statistics.median(numbers),
            'min': min(numbers),
            'max': max(numbers),
            'range': max(numbers) - min(numbers),
            'variance': round(statistics.variance(numbers), 4),
            'stdev': round(statistics.stdev(numbers), 4),
            'geometric_mean': round(math.exp(sum(math.log(x) for x in numbers)/len(numbers)), 4)
        }
        
        return jsonify(results)
    
    except (TypeError, ValueError) as e:
        return jsonify({'error': 'Tutti i parametri devono essere numeri validi (usare num1, num2, ecc.)'}), 400
    except statistics.StatisticsError as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)