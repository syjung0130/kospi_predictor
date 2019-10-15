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
 pip3 install virtualenv  

 - virtualenv 실행    
 (Linux or Mac) : source virtualenv/venv/bin/activate  
 (Window)       : call virtualenv\venv\Scripts\activate  
 
 - virtualenv 상에서 필요한 패키지 설치  
 pip3 install -r requirements.txt

 - 추가로 설치한 패키지가 있다면 설치된 패키지 추출  
 pip3 freeze > requirements.txt

 - 프로그램 실행  
 python3 main.py  

 - virtualenv 종료  
 deactivate

 - jupytern notebook 실행  
 pip3 install ipykernel  
 ipython kernel install --user --name=venv_kospi_predictor  
 pip3 install jupyter  
 pip3 freeze > requirements.txt  
 jupyter notebook  
 kospi_predictor.ipynb를 선택, 실행  
 (주의)  
 notebook실행 후, python kernel을 venv_kospi_predictor로 변경  
  
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
    - html reference url  
    일주일 전까지의 주식 정보만 조회할 수 있기 때문에, 'thistime=20190729093000' 문자열에서 날짜와 시간을 적절하게 수정해서 사용해야 한다.  
    https://finance.naver.com/item/sise_time.nhn?code=035420&amp&thistime=20190729093000&amp&page=1
      
  
  * 일 단위의 데이터 수집(완료)
    - 야후or구글(일봉) API 를 활용해서 database 형태로 가져오는 기능(구현 완료)
    - 최대 몇일까지 수집이 가능한지는 파악 필요: 검색해봤으나 알수없다. 테스트해보니 10년 까지는 수집이 가능하다.
    최대 10년까지 수집가능하도록 하자. 상장한지 10년이 안된 종목의 경우 상장일을 얻어오는 방법이 필요하다.
    한국증권거래소의 정보를 활용하면 될 듯하다.
        
  * 데이터 재가공(완료)  
  시간/분 단위로 수집한 데이터를 동일한 포맷의 Database로 재가공
    - 수집한 데이터를 Database로 저장(data 학습 및 예측부, 예상 가격 출력부 에서 사용)
    - 시가, 종가, 분 단위 가격, 거래량, 차트 상태(고점/저점/상향/하향), 투자 결정(매도/매수/관망)
    - 데이터를 읽어서 해당 시점에 대한 차트 상태(고점/저점/상향/하향) 정보 colum 추가
    - 차트 상태(고점/저점/상향/하향)정보에 따라 투자 결정(매도/매수/관망)을 판단해서 colum 추가(데이터 라벨링)
    - 일단위의 재가공 기능은 구현 완료, 분 단위의 재가공 기능 구현 완료
    
  * 참고 자료
    - db browser util: https://sqlitebrowser.org/
    - pandas-reader 사용방법 참고(yahoo 일봉 data): https://wikidocs.net/5753
    - naver web crawling reference html 얻는 방법: finance.naver.com접속 -> 종목코드 입력 -> 차트 아래의 '종합정보' 옆의 '시세 차트 클릭 -> '시간별 시세' 표를 우클릭 후, 프레임소스 보기 클릭

  
 ### 주식 가격 훈련, 예측  
 #### 목표
  - 선형적으로 가격을 학습, 얘측
  - 주기를 학습해서 매도/매수/관망을 분류
  - 선형적인 값 예측과 주기로 상/하향/변곡점 예측할 것인지는 옵션을 사용자가 결정할 수 있도록
  
 #### 개발 환경(완료)
  - Keras + tensorflow 2.0: 초기 구현은 keras로 구현, 모델을 튜닝하면서 필요할 경우 tensorflow를 사용
  - virtualenv
  - jupyter notebook(virtualenv)

 #### 상세 기능(진행)
  - DNN, regression
  - 선형적으로 예상 가격을 훈련, 예측하는 기능(regression)
  - 주기를 학습해서 상향/하향/관망을 훈련,예측하는 기능(classification, 다중분류 또는 RNN)
  - 가격을 예측, 예측한 데이터를 Numpy array로 저장(chart viewer에서 출력할 수 있도록)
  - 분기별 재무정보(영업이익, 현금 등)를 활용하는 방법 검토 필요(가중치에 상수값으로 ?)
  * 참고자료
  https://www.tensorflow.org/tutorials/keras/basic_regression?hl=ko
  
 ## 회고
  - 분 단위의 데이터보다는 일 단의의 일봉 데이터만으로도 충분할 것으로 보인다.
  - 시가, 종가, 거래량 만으로는 데이터가 부족하다. --> 증권거래소 API를 연동해서 재무정보를 얻어오는 방법이 필요하다.
  - 그래프의 선형적인 값을 예측하는 것(회귀)도 좋지만, 한 종목에 대한 장기간의 그래프를 보면, 상승과 하락을 반복하며 상승하거나 하락한다.
  상승폭이나 하락폭에 대해서도 학습을 할 수 있는 방법에 대해 연구가 필요하다. 
  - 데이터를 조작해서 모델에 주입하고 학습은 시킬 수 있는 수준이지만, 모델의 성능을 튜닝하는 방법에 대해 더 스터디가 필요하다.
  - 보완할 부분에 대해 회고하고 기획하는 시간이 필요하다.
 
 ### 차트 예측 viewer(예정)
 #### 목표
 이번 한 주의 예상 차트를 시/일 단위로 출력
 #### 상세 요구 사항
 - 웹서버를 연동해서 GUI를 구현 예정
