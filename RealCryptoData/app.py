from flask import Flask,render_template
from getCryptoData import CryptoData

app = Flask(__name__)

@app.route("/")
def index():
    cryptoData = CryptoData.get_cryptocurrencies()
    print()
    print(cryptoData)
    print()
    return render_template("index.html",data=cryptoData)

app.run(debug=True)
