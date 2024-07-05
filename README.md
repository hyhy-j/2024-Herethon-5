# 2024-Herethon-5

2024 여기톤 : HERETHON 5조
</br></br>

## 서비스 소개

![로고](https://github.com/2024-HERETHON/2024-Herethon-5/assets/90364700/94d8b64a-4c28-4911-81d5-39cc8df4a8f7)

💡 **키워드: MZ**

팝플레이스는 MZ세대를 위한 팝업스토어 정보 플랫폼입니다. 다양한 팝업스토어의 정보를 한곳에서 쉽게 찾아보세요. 소상공인과 개인 예술가들의 독특한 팝업스토어도 만나볼 수 있으며, 카테고리별 검색과 지도 기능을 통해 원하는 팝업스토어를 빠르게 찾을 수 있습니다. 방문한 팝업스토어에서 도장을 모으는 재미있는 기능도 제공되어 특별한 경험을 쌓을 수 있습니다. 또한, 지속가능성 평가 기능을 통해 팝업스토어의 환경 및 사회적 가치를 평가하여 더 나은 팝업스토어를 만들 수 있습니다. 팝플레이스와 함께 최신 트렌드의 팝업스토어를 즐기고, 특별한 순간을 만들어보세요!
</br></br>

## 기술 스택

<span>프론트엔드: </span> <img src="https://img.shields.io/badge/html-E34F26?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/css-1572B6?style=for-the-badge&logo=css3&logoColor=white"> <img src="https://img.shields.io/badge/javascript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">

<span>백엔드: </span><img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=Django&logoColor=white">

<span>기획·디자인: </span> <img src="https://img.shields.io/badge/figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white">
</br></br>

## 팀원 소개

| 역할        | 이름   | 소속                              |
| ----------- | ------ | --------------------------------- |
| 기획·디자인 | 전지영 | 동덕여자대학교 데이터사이언스전공 |
| 프론트엔드  | 김서윤 | 덕성여자대학교 소프트웨어전공     |
| 프론트엔드  | 이현정 | 숙명여자대학교 인공지능공학부     |
| 백엔드      | 손세영 | 성신여자대학교 융합보안공학과     |
| 백엔드      | 김희원 | 서울여자대학교 정보보호학과       |

</br>

## 폴더 구조

```
📂 2024-Herethon-5
├── README.md
├── accounts
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── db.sqlite3
├── manage.py
├── media
│   └── popup_images
├── popplace
│   ├── __init__.py
│   ├── __pycache__
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── templates
│   │   └── frontend
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static
│   ├── css
│   ├── img
│   └── js
└── yeougithon5
    ├── __init__.py
    ├── __pycache__
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

</br>

## 개발환경에서의 실행 방법

```
$ cd 2024-Herethon-5
$ python -m venv myvenv
$ source myvenv/Scripts/activate
$ pip install django-environ
$ pip install Pillow
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

  <hr/>
