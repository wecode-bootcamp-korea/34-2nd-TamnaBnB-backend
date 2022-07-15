## ✅ 프로젝트 소개
---

<br>

### 프로젝트 개요

위코드 부트캠프의 두번째 팀 프로젝트입니다.

이번 프로젝트 기간은 2022-07-04 ~ 2022-07-15까지 총 2주의 기간을 가졌습니다.

[Airbnb](https://www.airbnb.co.kr/)라는 숙소 호스팅 및 예약 사이트를 모티브로 하여 웹사이트에서 필요한 다양한 기능을 구현해보았습니다.

저작권 문제를 고려하여 프로젝트에 필요한 이미지는 [pixabay](https://pixabay.com/ko/)의 이미지를 사용하였습니다.

API 문서 바로가기 : [Postman API Document](https://documenter.getpostman.com/view/21494356/UzQrQmra)  

<br>

### 프로젝트 목표

1. Python의 Django 프레임워크를 활용한 백엔드 서버 구축하기.

2. MySQL을 활용하여 데이터베이스를 구축하고, Django의 ORM 최적화 방식 이해 및 적용하기.

3. 다양한 협업 툴을 사용하여 커뮤니케이션 역량 강화 및 발휘하기.

4. Scrum 방식 업무를 토대로 서비스를 배포하기 위한 빠른 개발 업무 해보기.

<br>

### 역할 분담

Front-end 개발자 4명, Back-end 개발자 1명으로 프로젝트를 진행하였습니다.

[김상웅] [sangwoong03](https://github.com/sangwoong03)

- `PM` / `Backend Developer`
1) 전세계를 대상으로 서비스 중인 `airbnb`는 전세계 고객을 대상으로 합니다.
기간과 동료들의 개발 능력을 고려하여 프로젝트에서는 지역을 제주도로 한정하였습니다.
2) 2주간 구현할 수 있는 필수 구현 사항과 추가 구현 사항을 구분하여 프로젝트 미팅을 진행하였습니다.
3) Stand-up meeting 간 Trello를 활용하여 Sprint 목표 진행 정도를 파악하고 업무를 재분담하였습니다.

- dbdiagram을 활용한 모델링

- Django 프로젝트 초기 설정

- 카카오 소셜 로그인 API 구현

- 숙소 전체/상세페이지 API 구현

- 후기 등록 및 조회 API 구현

- 예약 등록 및 조회 API 구현

- AWS (EC2, RDS) API 서버 배포

<br>
<br>

## ✅ 협업 Tool
---

<br>

### 📌 Git / Github

<br>

협업 툴 중 버전을 관리하기 위해 `Git`과 `Github`을 사용하였습니다.

이번 레포지토리는 혼자 사용하지만 `git rebase` 명령어를 사용하고 쓰임의 목적에 대해 이해할 수 있었습니다.

Github 레포지토리는 다음과 같습니다:

Front-end 레포지토리 [바로가기](https://github.com/wecode-bootcamp-korea/34-2nd-TamnaBnB-frontend)

<br>

### 📌 Trello

<br>

![](https://velog.velcdn.com/images/sangwoong/post/207bf245-e867-4713-891a-cd436ad44bea/image.gif)

1, 2주차의 Sprint 목표와 업무 진행을 파악하기 위한 Tool로 `Trello`를 사용했습니다.

`backlog` 프로젝트 미팅을 하며 전체 업무를 기능별로 세분화하여 전체 티켓을 발행했습니다.

`Sprint Goal` 일주일을 기준으로 진행해야 할 업무 티켓을 가리킵니다.

`In progress` 현재 개발 중인 업무 티켓을 가리킵니다.

`In review` Github에 PR을 올리고 리뷰와 merge 대기를 하는 작업을 가리킵니다.

`Done` merge가 완료되고 정상적으로 작동하는 기능을 가리킵니다.

`Blocker` 개발의 속도가 더디거나, 해결해야하는 문제들을 가리킵니다.

<br>

### 📌 Notion

<br>

![](https://velog.velcdn.com/images/sangwoong/post/d4693ad6-24cd-4db1-8e7a-5e18ebc081a5/image.png)

업무 간 반복되는 소통을 줄이고 정보를 공유하기 위해 `Notion`을 사용했습니다.

매일 진행되는 미팅의 내용을 기록하고 통신에 필요한 데이터 정보를 공유하기 위해 사용했습니다.

<br>

### 📌 Postman

<br>

![](https://velog.velcdn.com/images/sangwoong/post/34641aad-581f-4022-b9c4-7dfa5cde0007/image.png)

[Postman API Document](https://documenter.getpostman.com/view/21494356/UzQrQmra)

혼자 백엔드 개발을 하면서 소통과 개발과 로컬 서버 가동을 동시에 해야하는 경우가 있었습니다.

이런 경우 개발 속도가 지체되거나 소통에 집중을 할 수 없는 상태가 되어, 필요한 API 정보를 postman을 활용하여 문서로 소통하였습니다.

필요한 부분에 대해서만 회의를 하거나, 의사소통을 나눌 수 있어 효율적인 개발을 할 수 있었습니다.

<br>
<br>

## ✅ 기술 스택
---

이번 프로젝트에서 사용한 기술 스택은 다음과 같습니다.

|                                                Language                                                |                                                Framwork                                                |                                               Database                                               |                                                     ENV                                                      |                                                   HTTP                                                   | Deploy
| :----------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------: |---|
| <img src="https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white"> | <img src="https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white"> | <img src="https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=black"> | <img src="https://img.shields.io/badge/miniconda3-44A833?style=for-the-badge&logo=anaconda&logoColor=white"> | <img src="https://img.shields.io/badge/postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white"> | <img src="https://img.shields.io/badge/AWS-232F32?style=for-the-badge&logo=AmazonAWS&logoColor=white">  <img src="https://img.shields.io/badge/EC2-FF900?style=for-the-badge&logo=AmazonEC2&logoColor=white">  <img src="https://img.shields.io/badge/RDS-527FFF?style=for-the-badge&logo=AmazonEC2&logoColor=white">

<br>
<br>

## ✅ 구현 기능
---

이번 프로젝트에서 구현한 필수 구현 사항은 엔드포인트로 나누어 보았을 때,
크게 4가지로 볼 수 있습니다.

> 1. 카카오 - 소셜 로그인 API

- 카카오 API를 통해 소셜로그인을 구현했습니다. ([Kakao Developers](https://developers.kakao.com/) 문서 참조)

- 클라이언트(FE)로부터 카카오 로그인 인가 코드를 받아옵니다.

- 받아온 인가코드를 통해 카카오 서버에 카카오 토큰을 요청합니다. `requests.get`

- 받아온 카카오 토큰을 통해 다시 한번 카카오 서버에 유저 정보를 요청합니다. `requests.get`

- 받아온 유저 정보에 접근하여 필요한 데이터를 DB상에 저장합니다.

- 로그인을 성공적으로 수행했을 경우 서버에서 발행한 토큰을 클라이언트에게 발급합니다.

<br>

> 2-1. 숙소 전체리스트 API

- 메인페이지 url로 접근 시 숙소의 전체 리스트를 제공합니다.

- 지역, 예약 날짜, 인원수에 따라 숙소를 필터링합니다. (`Query Parameter`)
 
- 유형, 카테고리, 가격범위를 통해 숙소를 필터링합니다. (`Query Parameter`)

(ORM 최적화를 통해 필터링과 필요한 정보를 효율적으로 제공하기 위한 노력..)

<br>

> 2-2. 숙소 상세페이지 API

- 메인페이지에서 특정 숙소의 정보를 요청하고 해당 정보를 제공합니다. (`Path parameter`)

- 상세 정보에는 숙소의 정보, 리뷰, 호스트, 예약 내역을 함께 제공합니다.

<br>

> 3. 후기 API

- 로그인을 한 유저에 한하여 숙소의 후기를 작성할 수 있습니다.

- 숙소의 상세페이지로 접근하면 숙소의 전체 리뷰, 개수, 평점을 확인할 수 있습니다.

++ 보완사항
 
 - 숙소를 실제로 이용한 유저에 한하여 후기를 작성할 수 있도록 수정이 필요합니다. 

<br>

> 4. 예약 API

- 로그인을 한 유저에 한하여 숙소를 예약할 수 있습니다.

- 예약 정보는 체크인/체크아웃 날짜, 인원 수, 가격, 숙소의 정보를 필요로합니다.

++ 보완사항

- 현재는 로그인을 한 유저에게 포인트를 제공하여 숙소의 가격만큼 차감하는 방식으로 결제를 진행합니다.

- 마찬가지로 소셜 결제 API를 사용하여 보완할 수 있겠습니다.

<br>
<br>

## ✅ 추가 구현 사항

> 1. 위시리스트 API

- 사용자가 맘에 드는 숙소를 찾으면 위시리스트에 해당 숙소를 저장하는 기능입니다.

- 커머스 사이트의 장바구니 기능과 비슷합니다.

<br>

> 2. 호스트되기 API

- 사실 에어비앤비의 가장 중요하고 메인 기능이라고 할 수 있는 것은 `호스트`되기 기능입니다.

- 유저인 동시에 숙소를 운영하는 호스트 정보를 등록할 수 있는 기능입니다.

- 호스트의 이름, 닉네임, 숙소 사진 등을 활용하여 호스트 ID를 생성할 수 있습니다.

<br>

> 3. S3를 활용한 이미지 저장


현재 개발 중에 있는 구현으로 aws의 S3 기능을 통해 이미지 url을 저장하는 기능을 구현하고자 합니다.