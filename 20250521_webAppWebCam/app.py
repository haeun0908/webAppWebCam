from flask import Flask, render_template, request, redirect, url_for
import csv
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 홈 페이지 (입력 폼)
@app.route('/')
def index():
    return render_template('index.html')

# 데이터 처리 및 저장
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('pyname')
    phone = request.form.get('pyphone')
    birthday = request.form.get('pybirthday')

    # 파일 업로드 처리
    photo = request.files.get('photo')
    photo_filename = ''
    if photo and photo.filename:
        photo_filename = name + '_' + photo.filename
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)

    # 웹캠 사진 처리
    webcam_photo = request.form.get('webcam_photo')
    webcam_photo_filename = ''
    if webcam_photo:
        # Base64 디코딩
        webcam_photo_data = webcam_photo.split(',')[1]  # "data:image/png;base64," 제거
        webcam_photo_bytes = base64.b64decode(webcam_photo_data)
        webcam_photo_filename = f"{name}_webcam.png"
        webcam_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], webcam_photo_filename)
        with open(webcam_photo_path, 'wb') as f:
            f.write(webcam_photo_bytes)

    # addbook.txt 파일에 CSV 형식으로 저장 (사진 파일명도 저장)
    with open('addbook.txt', 'a', newline='', encoding='utf-8') as 파일:
        작성자 = csv.writer(파일)
        작성자.writerow([name, phone, birthday, photo_filename, webcam_photo_filename])

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)