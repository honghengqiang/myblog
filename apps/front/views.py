from flask import Blueprint, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
from .forms import UpLoadForm
from werkzeug.datastructures import CombinedMultiDict
from PIL import Image, ImageFilter, ImageDraw, ImageFont

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


@bp.route('/change')
def change():
    url = "change.png"
    filename = request.args.get('filename')
    name = request.args.get('title')
    text = list(name)
    # pic2Text(filename, text)

    img = Image.open(UPLOAD_PATH + '/' + filename).convert("RGBA")
    w = 100  # 宽度固定
    h = int((float(img.size[1]) / float(img.size[0])) * w)  # 高度按比例得出
    fontSize = 20  # 输出字体大小
    img.thumbnail((w, h))  # 获取缩略图
    src = img.convert('L')  # 转换成灰度图
    minGrey = 255  # 最小灰度
    maxGrey = 0  # 最大灰度
    greyMap = [[0 for col in range(h)] for row in range(w)]  # 灰度图 注意 w h
    # 此处循环求得灰度表以及最大最小灰度值
    for i in range(w):
        for j in range(h):
            greyMap[i][j] = src.getpixel((i, j))  # 获取每一个点的灰度值
            if greyMap[i][j] > maxGrey:  # 获取最大灰度
                maxGrey = greyMap[i][j]
            if greyMap[i][j] < minGrey:  # 获取最小灰度
                minGrey = greyMap[i][j]
    # 计算灰度间隔
    greyStep = (maxGrey - minGrey) / len(text)
    # 此处生成文字图片,注意输出的时候 w 和 h
    output = Image.new('RGBA', (w * fontSize, h * fontSize), (255, 255, 255))
    draw = ImageDraw.Draw(output)
    ft = ImageFont.truetype(UPLOAD_PATH + "/msyhbd.ttf", fontSize)  # 注意字体支持中文
    for j in range(h):
        for i in range(w):
            index = int((greyMap[i][j] - minGrey) // greyStep)  # 计算出改点使用哪个字符
            if index >= len(text):
                index = len(text) - 1  # 注意结尾最大灰度值，防止越界
            draw.text((i * fontSize, j * fontSize), text[index], fill=img.getpixel((i, j)), font=ft)  # 汉字编码
        # output.save(file.split('.')[0] + '_text.png', 'PNG')
    output.save(UPLOAD_PATH + "/" + url, 'PNG')
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
