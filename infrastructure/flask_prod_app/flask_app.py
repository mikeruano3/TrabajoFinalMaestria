from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import papermill as pm
import os
from ast import literal_eval
from web_scrap import scrappearPersonaEnElPeriodico
from ask_nlp import askQuestion, initNlp

nlp = None
app=Flask(__name__, static_folder='static')
CORS(app, support_credentials=True)

@cross_origin(supports_credentials=True)
@app.route('/',  methods=['GET'])
def index():
    return jsonify('PredictionAPI')

# Ejecuta el notebook usando la celda taggeada parameters y la celda taggeada output
def notebookExecuter(nbName, outputName, parametersDict):
    nbresult = pm.execute_notebook(
        os.path.join(app.static_folder, 'notebooks/' + nbName + '.ipynb'),
        os.path.join(app.static_folder, 'notebooks/outputs/' + outputName + '.ipynb'),
        parameters = parametersDict
    )
    return nbresult

# Busca el objeto de resultado en la celda taggeada como output
def notebookSearchResultText(nbresult):
    searchresult = list(cell for cell in nbresult.cells for celldata in cell['metadata']['tags'] if celldata == 'output')
    prediction = None
    if searchresult[0]:
        prediction = searchresult[0]['outputs'][0]['text']
    return str(prediction)[0:-1]

def locallyInitGlobalNLP():
    global nlp
    if not nlp:
        nlp = initNlp()

# ejecuta el PLN por partes
def PLNExecuter(peopleList):
    print("obteniendo scraping")
    web_scrapping_result = scrappearPersonaEnElPeriodico(peopleList)
    print("noticias obtenidas", web_scrapping_result)
    #locallyInitGlobalNLP()
    #global nlp
    print("inicializando nlp")
    nlp = initNlp()
    print("resolviendo preguntas")
    result = askQuestion(nlp, web_scrapping_result)
    return result

# Scrapping por persona
def ScrapExecuter(peopleList):
    #web_scrapping = notebookExecuter('web_scrapping', 'web_scrapping_output', dict(peopleList=peopleList))
    #web_scrapping_result = literal_eval(notebookSearchResultText(web_scrapping))
    web_scrapping_result = scrappearPersonaEnElPeriodico(peopleList)
    return dict(status=200, data=web_scrapping_result)

@cross_origin(supports_credentials=True)
@app.route('/scrap', methods = ['POST'])
def scrap():
    if request.method == 'POST':
        content = request.json
        people = content['people']
        result = ScrapExecuter(people)
        return result

@cross_origin(supports_credentials=True)
@app.route('/predict', methods = ['POST'])
def predict():
    if request.method == 'POST':
        print("Inicializando pedido de prediccion")
        content = request.json
        people = content['people']
        result = PLNExecuter(people)
        #return jsonify(result)
        return result

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) or 5000
    #app.run(debug=True, host='0.0.0.0', port=port)
    host = "0.0.0.0"
    from waitress import serve
    print('Running server on ', host, ':', port)
    serve(app, host=host, port=port)