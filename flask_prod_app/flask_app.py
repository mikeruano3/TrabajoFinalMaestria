from flask import Flask, render_template, request, jsonify
import papermill as pm
import os

app=Flask(__name__, static_folder='static')

@app.route('/')
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

@app.route('/predict', methods = ['POST'])
def result():
    if request.method == 'POST':
        content = request.json
        word_to_search = content['word_to_search']
        question_object = content['question_object']
        result = NotebookExecuter(word_to_search, question_object)
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=False)