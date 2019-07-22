# KOSPI Predictor

## Docker 실행 방법
- docker build
cd docker  
docker build -t scrapper:imx-1 .  
- docker container 실행  
./run_container.sh . 
- 프로그램 실행  
../pybuild.sh
 - Docker 컨테이너 모두 삭제  
 docker rm $(docker ps -a -q)
 - Docker 이미지 모두 삭제  
 docker rmi $(docker images -q)
 - 특정 이미지만 삭제  
 (image 리스트 확인)  
 docker images  
 (특정 이미지를 삭제)  
 docker rmi 이미지id  

## virtualenv 실행 방법
 - virtualenv 패키지 설치
 cd virtualenv
 pip3 install virtualenv

 - virtualenv 실행
 virtualenv venv
 source venv/bin/activate

 - virtualenv 상에서 필요한 패키지 설치
 pip3 install -r requirements.txt

 - 추가로 설치한 패키지가 있다면 설치된 패키지 추출
 pip3 freeze > requirements.txt

 - virtualenv 종료
 deactivate

## 개요
KOSPI 가격을 예측하는 프로그램.


## 전체 구성도
 ### 데이터 수집(데이터 마이닝)
 #### 목표
  - 금융 정보의 데이터를 크롤링해서 특정 기간의 데이터(시가, 종가, 거래량)를  시/일 단위로 DB로 저장
 #### 상세 기능
  종목 코드는 우선 한 종목 코드로 고정해서 기능을 구현
  * 분 단위의 데이터 수집(완료)
    - 분 단위의 데이터는 네이버 금융(시간별 데이터)페이지를 크롤링해서 수집한다.
    - 시간별 분석의 경우, 분 단위까지의 데이터를 수집할 수 있고, 1주일치의 데이터만 가져올 수 있는 제한이 있다.
      (9시부터 15시까지 6시간 * 60분, 즉 360개의 데이터를 하루에 수집할 수 있다)
    - 시간/분 단위의 단타 투자 시의 가격 예측을 위해 분 단위의 데이터 수집한다.(수집 기능 구현 완료)
    - 종목을 선택 후, 분단위의 정밀 분석은 1주간의 데이터를 수집, 학습 후, 1주 후부터 예측이 가능하도록 한다.
  
  * 일 단위의 데이터 수집(완료)
    - 야후or구글(일봉) API 를 활용해서 database 형태로 가져오는 기능(구현 완료)
    - 최대 몇일까지 수집이 가능한지는 파악 필요: 검색해봤으나 알수없다. 테스트해보니 10년 까지는 수집이 가능하다.
    최대 10년까지 수집가능하도록 하자. 상장한지 10년이 안된 종목의 경우 상장일을 얻어오는 방법이 필요하다.
    한국증권거래소의 정보를 활용하면 될 듯하다.
        
  * 데이터 재가공(TODO)  
  시간/분 단위로 수집한 데이터를 동일한 포맷의 Database로 재가공
    - 수집한 데이터를 Database로 저장(data 학습 및 예측부, 예상 가격 출력부 에서 사용)
    - 시가, 종가, 분 단위 가격, 거래량, 차트 상태(고점/저점/상향/하향), 투자 결정(매도/매수/관망)
    - 데이터를 읽어서 해당 시점에 대한 차트 상태(고점/저점/상향/하향) 정보 colum 추가
    - 차트 상태(고점/저점/상향/하향)정보에 따라 투자 결정(매도/매수/관망)을 판단해서 colum 추가(데이터 라벨링)
    
  * refactoring(완료)
    - datetime 연동부를 별도의 Helper모듈로 구현(time 관련 로직을 한군데서 수정할 수 있도록): 완료
    - Collector Base class 구현: 완료
    - Database 재가공부를 별도의 모듈로 분리: 완료
    
  * 참고 자료
    - db browser util: https://sqlitebrowser.org/
    - pandas-reader 사용방법 참고(yahoo 일봉 data): https://wikidocs.net/5753
    - naver web crawling reference html 얻는 방법: finance.naver.com접속 -> 종목코드 입력 -> 차트 아래의 '종합정보' 옆의 '시세 차트 클릭 -> '시간별 시세' 표를 우클릭 후, 프레임소스 보기 클릭

  
 ### 주식 가격 훈련, 예측
 #### 목표
  - 시가, 종가, 거래량을 토대로 차트를 학습해서 다음 날의 '시' 단위로 가격을 예측
  - 이번 한 '주' 단위까지 예측해서 예상 차트 데이터 생성
  - 예측된 주식 가격값을 토대로 1주 뒤까지의 시간마다의 가격을 DB로 저장 (예상차트출력부에서 활용할 수 있도록)
 #### 상세 요구사항
  - linear regression을 사용해서 가격을 예측, 예측한 데이터를 Numpy array로 저장
  - linear regression을 통해 학습한 데이터를 통해 매수/매도/관망 등의 분류를 할 수 있도록 다른 모델(RNN or CNN ?)의 입력으로 사용
  - 예측데이터(Numpy array), 매수/매도/관망 을 DB로 생성(차트 출력부에서 확용할 수 있도록)
  - 분기별 재무정보(영업이익, 현금 등)를 활용하는 방법 검토 필요(가중치에 상수값으로 ?)
  
  
 ### 차트 예측 viewer
 #### 목표
 이번 한 주의 예상 차트를 시/일 단위로 출력
 #### 상세 요구 사항
 - 이번 한 주의 예상 차트를 시/일 단위로 출력
 - GUI 프레임워크는 맥과 윈도우에서 모두 사용이 가능한 Qt를 이용
 - 실제 현재 주식그래프를 비교 데이터로 출력(추후 서버 연동 시)
 - 서버 연동을 할 경우, 웹에서 출력
  

 ### 챗봇
 - 슬랙 API를 활용해서 종목에 대한 예측정보(시간별 예상 가격)를 텍스트로 답장
