# webAppWebCam
이 Flask 웹 애플리케이션은 이름, 전화번호, 생일, 업로드된 사진 및 웹캠 사진을 입력받아 처리하고 저장합니다.<br>
입력된 데이터는 addbook.txt 파일에 CSV 형식으로 저장되며, 사진 파일은 uploads 폴더에 저장됩니다.<br>

## 1. 프로그램 준비 및 새로운 작업 환경 만들기
1. 새 폴더 생성<br><br>
![새 폴더 생성](https://github.com/haeun0908/webAppWebCam/blob/main/images/%EC%83%88%20%ED%8F%B4%EB%8D%94%20%EC%83%9D%EC%84%B1.png)<br>

2. 가상 환경 생성 및 활성화<br>
```
conda create -n webApp python=3.9
```

3. Flask 프레임워크 설치<br>
```
pip install flask
```

## 2. 파일 구조
Flask 애플리케이션은 특정 폴더 구조를 따릅니다.<br>
HTML 파일은 templates 폴더에, 정적 파일(CSS, 이미지 등)은 static 폴더에 위치해야 합니다.<br><br>
![파일 구조](https://github.com/haeun0908/webAppWebCam/blob/main/images/%ED%8C%8C%EC%9D%BC%20%EA%B5%AC%EC%A1%B0.png)<br>

- app.py: Flask 애플리케이션의 메인 Python 코드 파일입니다.
- addbook.txt: 사용자 데이터를 CSV 형식으로 저장할 파일입니다.<br>
  초기에는 비어 있으며, 애플리케이션 실행 시 자동으로 생성됩니다.
- static/uploads: 업로드된 사진 및 웹캠 사진 파일이 저장될 폴더입니다.
- templates/index.html: 사용자 입력을 받는 웹 페이지의 HTML 파일입니다.

## 3. 프로그램 완성 및 기능 구현
1. 웹 브라우저를 열고 http://127.0.0.1:5000 주소로 접속합니다.<br>
2. 웹 페이지에 표시된 입력 폼에 이름, 전화번호, 생일을 입력합니다.<br>
3. 사진 파일을 업로드하거나 웹캠을 사용하여 사진을 촬영합니다.<br>
4. "제출" 버튼을 클릭하여 데이터를 저장합니다.<br><br>
![프로그램 완성 및 기능 구현1](https://github.com/haeun0908/webAppWebCam/blob/main/images/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%20%EC%99%84%EC%84%B1%20%EB%B0%8F%20%EA%B8%B0%EB%8A%A5%20%EA%B5%AC%ED%98%841.png)<br>

5. 입력된 데이터는 addbook.txt에, 사진 파일은 uploads 폴더에 저장되는 것을 확인할 수 있습니다.<br><br>
![프로그램 완성 및 기능 구현2](https://github.com/haeun0908/webAppWebCam/blob/main/images/%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%20%EC%99%84%EC%84%B1%20%EB%B0%8F%20%EA%B8%B0%EB%8A%A5%20%EA%B5%AC%ED%98%842.png)<br>

## 4. 주요 코드 설명
### app.py
- Flask 애플리케이션을 초기화하고, 업로드된 파일이 저장될 폴더(static/uploads)를 설정합니다.<br>
  만약 폴더가 없다면 자동으로 생성합니다.
```
# Flask 앱 초기화 및 설정
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
```

- 기본 경로('/')로 접속했을 때 templates 폴더의 index.html 파일을 렌더링하여 사용자에게 보여줍니다.
```
# 홈 페이지 라우트
@app.route('/')
def index():
    return render_template('index.html')
```

- /submit 경로로 POST 요청이 들어왔을 때 실행되는 함수입니다.<br>
  웹 페이지 폼에서 사용자가 입력한 이름, 전화번호, 생일 데이터를 가져옵니다.
```
# 데이터 처리 및 저장
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('pyname')
    phone = request.form.get('pyphone')
    birthday = request.form.get('pybirthday')
```

- 사용자가 업로드한 photo 파일을 받아와 지정된 업로드 폴더(static/uploads)에 저장합니다.<br>
  파일 이름은 사용자 이름과 원본 파일 이름을 조합하여 생성합니다.
```
    # 파일 업로드 처리
    photo = request.files.get('photo')
    if photo and photo.filename:
        photo_filename = name + '_' + photo.filename
        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
        photo.save(photo_path)
```

- 웹캠에서 촬영하여 Base64 형식으로 전달된 webcam_photo 데이터를 디코딩합니다.<br>
  디코딩된 이미지 데이터를 PNG 파일로 변환하여 업로드 폴더에 저장합니다.<br>
  파일 이름은 사용자 이름과 'webcam.png'를 조합합니다.
```
    # 웹캠 사진 처리
    webcam_photo = request.form.get('webcam_photo')
    if webcam_photo:
        webcam_photo_data = webcam_photo.split(',')[1]
        webcam_photo_bytes = base64.b64decode(webcam_photo_data)
        webcam_photo_filename = f"{name}_webcam.png"
        webcam_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], webcam_photo_filename)
        with open(webcam_photo_path, 'wb') as f:
            f.write(webcam_photo_bytes)
```

- 사용자의 이름, 전화번호, 생일, 저장된 사진 파일 이름, 저장된 웹캠 사진 파일 이름을 addbook.txt 파일에 CSV 형식으로 추가합니다.<br>
  파일은 'a' 모드(append)로 열어 기존 내용에 덧붙입니다.
```
    # addbook.txt 파일에 데이터 저장
    with open('addbook.txt', 'a', newline='', encoding='utf-8') as 파일:
        작성자 = csv.writer(파일)
        작성자.writerow([name, phone, birthday, photo_filename, webcam_photo_filename])
```

- 이 스크립트가 직접 실행될 때 Flask 애플리케이션을 실행합니다.<br>
  debug=True 옵션은 개발 중에 유용하며, 코드 변경 시 서버가 자동으로 재시작됩니다.
```
if __name__ == '__main__':
    app.run(debug=True)
```

### index.html
- JavaScript navigator.mediaDevices.getUserMedia API를 사용하여 사용자의 웹캠 비디오 스트림에 접근합니다.<br>
  스트림을 가져오면 \<video> 요소에 연결하여 실시간으로 웹캠 영상을 표시합니다.<br>
  웹캠 접근에 실패하면 콘솔에 오류 메시지를 출력합니다.
```
<!-- 웹캠 스트림 시작 -->
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
    })
    .catch(err => {
        console.error("웹캠 접근 실패:", err);
    });
```

- "촬영" 버튼을 클릭했을 때 실행되는 이벤트 리스너입니다.<br>
  현재 \<video> 요소에 표시되는 웹캠 프레임을 <canvas> 요소에 그립니다.<br>
  그린 이미지를 PNG 형식의 Base64 문자열로 변환하여 숨겨진 <input type="hidden"> 필드(webcamPhotoInput)에 저장합니다.<br>
  또한, 촬영된 이미지를 preview 요소에 표시하여 사용자에게 보여줍니다.
```
<!-- 사진 촬영 -->
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // 캔버스 데이터를 이미지로 변환
    const imageData = canvas.toDataURL('image/png');
    webcamPhotoInput.value = imageData;

    // 미리보기 업데이트
    const preview = document.getElementById('preview');
    preview.src = imageData;
    preview.style.display = 'block';
});
```
