from flask import Flask, render_template, request, jsonify
import papermill as pm
import os

app=Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return jsonify('PredictionAPI')

def ValuePredictor(alpha, ratio):
    nbresult = pm.execute_notebook(
        os.path.join(app.static_folder, 'notebooks/main_script.ipynb'),
        os.path.join(app.static_folder, 'notebooks/output_execution_test.ipynb'),
        parameters = dict(alpha=alpha, ratio=ratio)
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
        alpha = content['alpha']
        ratio = content['ratio']
        #to_predict_list = request.form.to_dict()
        #to_predict_list=list(to_predict_list.values())
        #to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(alpha, ratio)
        return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)