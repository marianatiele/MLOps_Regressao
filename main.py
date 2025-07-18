from flask import Flask, request, jsonify
from  flask_basicauth import BasicAuth
from textblob import TextBlob

#Segundo modelo Regressao Linear
#import pandas as pd
#from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle

colunas = ['tamanho', 'ano', 'garagem']
modelo  = pickle.load(open('modelo.sav', 'rb'))
#Modelo está serializado via Pickle
#Lendo os dados do Segundo modelo Regressão Linear
#dados = pd.read_csv('casas.csv', sep=',')


#dados = dados[colunas]

#x = dados.drop('preco', axis=1)
#y = dados['preco']

#x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, train_size=0.7, random_state=42)

#modelo  = LinearRegression()
#modelo.fit(x_treino, y_treino)

## Daqui pra baixo tudo é execultado e carregado sempre que atualizar a API
app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'Natiele'
app.config['BASIC_AUTH_PASSWORD'] = '@Lotus25'

basic_auth = BasicAuth(app)




@app.route('/')

def home():
    return 'Minha primeira rota'
#A frase precisa esta em inglês
@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    texto = TextBlob(frase)
    polaridade = texto.sentiment.polarity
    return 'Polaridade: {}'.format(polaridade)



@app.route('/preco/', methods = ['POST'])
def valor_casa():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])


app.run(debug=True)