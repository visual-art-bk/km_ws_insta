# Playwright 기반 웹 스크래핑 EXE 빌드 프로젝트

이 프로젝트는 [Playwright](https://playwright.dev/)를 활용하여 웹 스크래핑 작업을 수행하고, 이를 Windows 환경에서 실행 가능한 EXE 파일로 빌드하는 Python 프로그램입니다.

---

## 📖 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [기술 스택](#기술-스택)
3. [프로젝트 구조](#프로젝트-구조)
4. [설치 방법](#설치-방법)
5. [사용 방법](#사용-방법)
6. [빌드 및 배포](#빌드-및-배포)
7. [문제 해결](#문제-해결)
8. [라이선스](#라이선스)
9. [TO DO](#TO-DO)

---

## 프로젝트 소개

이 프로젝트는 다음과 같은 목적을 가지고 개발되었습니다:

- **웹 데이터 스크래핑**: 다양한 웹사이트에서 데이터를 자동으로 수집.
- **손쉬운 실행**: Python 환경 없이 Windows EXE 파일로 실행 가능.
- **유지보수 편리성**: 스크래핑 로직 및 Playwright 설정 파일이 명확하게 관리.

---

## 기술 스택

- **언어**: Python 3.10 이상
- **웹 자동화**: Playwright
- **EXE 빌드**: PyInstaller
- **패키지 관리**: pip

---

## 프로젝트 구조

```plaintext
project/
│
├── src/                # 주요 소스 코드 폴더
│   ├── app  scraper.py      # 웹 스크래핑 로직
│   ├── config.py       # 설정 파일 (URL, 스크래핑 옵션 등)
│   └── utils.py        # 유틸리티 함수
│
├── tests/              # 테스트 코드 폴더
│   └── test_scraper.py # Scraper 기능 테스트
│
├── requirements.txt    # 필요한 Python 패키지 목록
├── README.md           # 프로젝트 설명 파일
├── main.py             # 프로그램 진입점
└── build/              # PyInstaller 빌드 아웃풋 폴더

```

---

## 설치 방법

### 1. Python 설치

- Windows에 [Python 3.10 이상](https://www.python.org/downloads/)을 설치합니다.
- 설치 시 `PATH에 추가` 옵션을 활성화하세요.

### 2. 프로젝트 클론 및 패키지 설치

1. 아래 명령어를 실행하여 프로젝트를 클론합니다:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```
2. 필요한 Python 패키지를 설치합니다:
   ```bash
   pip install -r requirements.txt
   ```

### 3. Playwright 설치 및 브라우저 설정

1. Playwright를 설치합니다:
   ```bash
   playwright install
   ```
2. 필요한 브라우저를 설정합니다:
   ```bash
   playwright install chromium
   ```

---

## 사용 방법

### 1. 스크래핑 실행

스크래핑 로직은 `main.py`에서 실행됩니다.  
아래 명령어를 터미널에서 실행하세요:

```bash
python src/app/main.py
```

---

## 빌드 및 배포

### 1. PyInstaller 설치

Windows에서 EXE 빌드를 수행하기 위해 PyInstaller를 설치합니다.  
아래 명령어를 실행하세요:

```bash
pip install pyinstaller
```

---

## 문제 해결

### 1. Window 환경에서의 파이썬 가상공간 활성화 실패

`Activate.ps1cannot be loaded because running scripts is disabled on this system.` 라고 뜰 때:

./<가상환경명>/Scripts/activate 실행 시 활성화 실패하는 경우 아래 명령어를 실행해서 체크하세요:

```bash
Get-ExecutionPolicy
```

Restricted로 설정되어 있다면 실행 정책을 변경해야 합니다.

아래 명령어를 실행하세요:

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

다시 `./가상-공간-이름/Scripts/activate`를 실행해서 가상공간을 활성화합니다.

### 2. Playwright 브라우저 설치 실패

Playwright 설치 시 브라우저가 제대로 설치되지 않는 경우 아래 명령어를 실행하세요:

```bash
playwright install chromium
```

### 3. PyInstaller 빌드 실패

PyInstaller로 빌드 시 `import` 관련 에러가 발생할 경우, 아래 명령어를 실행하여 **숨겨진 모듈(hidden-import)**을 명시적으로 추가하세요:

```bash
pyinstaller --onefile --noconsole --hidden-import=playwright.sync_api main.py
```

---

## 라이선스

이 프로젝트의 저작권은 **[뤼초록]**에 있으며, 아래의 조건에 따라 사용이 허가됩니다:

1. **비상업적 사용**:  
   이 소프트웨어는 개인 또는 연구 목적으로 사용 가능합니다. 상업적 목적으로 사용하려면 **[뤼초록]**의 사전 허가가 필요합니다.

2. **수정 및 재배포 금지**:  
   소스 코드의 수정 및 재배포는 금지됩니다. 필요한 경우, **[뤼초록]**과 협의하여 허가를 받아야 합니다.

3. **책임 제한**:  
   이 소프트웨어는 "있는 그대로" 제공되며, 사용 중 발생한 어떠한 문제에 대해서도 **[뤼초록]**은 책임을 지지 않습니다.

---

### 문의

라이선스 관련 문의 사항은 아래 이메일로 연락해 주세요:

📧 **support@[rchr-lab].store**

---

## TO DO

### playwright

아래의 TODO 번호를 vscode의 Find in Folder 기능을 이용해 프로젝트에서 찾으세요.

- 3042

1. **사용자가 최초1회실행시**:
   인스톨 여부를 확인하고, 필요한 드라비버파일을 루트로 복사해온는 게 맞을까