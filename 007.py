"""
Author   : HarperHao
TIME    ： 2020/10/18
FUNCTION:  文件上传
"""
from flask import request, Flask

app = Flask(__name__)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')


