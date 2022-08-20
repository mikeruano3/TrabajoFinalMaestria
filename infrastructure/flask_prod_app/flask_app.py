from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import papermill as pm
import os

app=Flask(__name__, static_folder='static')
CORS(app, support_credentials=True)

@cross_origin(supports_credentials=True)
@app.route('/',  methods=['GET'])
def index():
    return jsonify('PredictionAPI')

def NotebookExecuter(word_to_search, question_object):
    nbresult = pm.execute_notebook(
        os.path.join(app.static_folder, 'notebooks/main_script.ipynb'),
        os.path.join(app.static_folder, 'notebooks/output_execution_test.ipynb'),
        parameters = dict(word_to_search=word_to_search, question_object=question_object)
    )
    searchresult = list(cell for cell in nbresult.cells for celldata in cell['metadata']['tags'] if celldata == 'output')
    prediction = ''
    if searchresult[0]:
        prediction = searchresult[0]['outputs'][0]['data']['text/plain']
    return prediction

@cross_origin(supports_credentials=True)
@app.route('/predict', methods = ['POST'])
def result():
    if request.method == 'POST':
        content = request.json
        word_to_search = content['word_to_search']
        question_object = content['question_object']
        result = NotebookExecuter(word_to_search, question_object)
        return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) or 5000
    app.run(debug=False, host='0.0.0.0', port=port)