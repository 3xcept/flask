from flask import Flask, render_template, request, jsonify
import io
import contextlib

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')

def safe_eval(code):
    # Create a restricted namespace
    namespace = {}
    
    # Redirect standard output to capture print statements
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        try:
            exec(code, namespace)
        except Exception as e:
            return str(e), False
    
    # Return captured output, stripped of trailing whitespace
    return output.getvalue().rstrip(), True


@app.route('/eval', methods=['POST'])
def evaluate_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({"error": "Code is required"}), 400

    code = data['code']

    # Evaluate the provided code
    output, success = safe_eval(code)

    if not success:
        return jsonify({"error": output}), 400

    return jsonify({"output": output}), 200

if __name__ == '__main__':
  app.run(port=5000)
