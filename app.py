from flask import Flask, render_template, request
from check import predict_score
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['movie_name']
        result = predict_score(name)
        data = json.loads(result)  # Sửa thành json.loads() để chuyển đổi chuỗi JSON thành đối tượng Python
        return render_template('index.html', result=data)
    else:
        return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run()