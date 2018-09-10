from flask import Blueprint, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from .forms import UpLoadForm
from werkzeug.datastructures import CombinedMultiDict
from PIL import Image, ImageFilter

bp = Blueprint('front', __name__)
UPLOAD_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static/ima')

i = 0

filename = None


@bp.route('/')
def index():
    return render_template('front/front_index.html')


@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('front/upload.html', filename=None)
    else:
        form = UpLoadForm(CombinedMultiDict([request.form, request.files]))
        if form.validate():
            # 获取描述信息
            global i
            # desc = request.form.get('desc')
            avatar = request.files.get('avatar')
            filename = secure_filename(avatar.filename)
            print(UPLOAD_PATH)

            avatar.save(os.path.join(UPLOAD_PATH, filename))
            # print(desc)
            print('文件上传成功')
            i = 0
            return render_template('front/upload.html', filename=filename)
        else:
            print(form.errors)
            return 'fail'


@bp.route('/rotate')
def rotate():
    filename = request.args.get('filename')
    print(filename)
    if filename:
        url = 'change.jpg'
        im = Image.open(UPLOAD_PATH + '/' + filename)
        im.rotate(45).save(UPLOAD_PATH + '/' + url)
        return jsonify({"filename": url})


@bp.route('/tongdao')
def tongdao():
    filename = request.args.get('filename')
    print(filename)
    if filename:
        url = 'change.jpg'
        im = Image.open(UPLOAD_PATH + '/' + filename)
        r, g, b = im.split()
        a = r
        r = g
        g = b
        b = a
        Image.merge('RGB', (r, g, b)).save(UPLOAD_PATH + '/' + url)
        return jsonify({"filename": url})


array = [ImageFilter.BLUR, ImageFilter.CONTOUR, ImageFilter.DETAIL,
         ImageFilter.EDGE_ENHANCE, ImageFilter.EDGE_ENHANCE_MORE,
         ImageFilter.EMBOSS, ImageFilter.FIND_EDGES, ImageFilter.SHARPEN,
         ImageFilter.SMOOTH, ImageFilter.SMOOTH_MORE]


@bp.route('/filter')
def filter():
    print('dfg fg ')
    global i, filename
    if i == 0:
        filename = request.args.get('filename')
    url = 'change.jpg'
    im = Image.open(UPLOAD_PATH + '/' + filename)
    im2 = im.filter(array[i])
    im2.save(UPLOAD_PATH + '/' + url)
    if i != 9:
        i = i + 1
    else:
        i = 0
    print(i)
    return jsonify({"filename": url})
