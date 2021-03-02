# Kaggle X-Ray project

### [일정 및 상황] trello : https://trello.com/b/bUIob804/kaggle  
    
#### Kaggle X-ray 이상징후 분석 프로젝트(VinBigData Chest X-ray Abnormalities Detection)   
       url : https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection   
       발표 총 3번: 16, 19, 26일   
       참가 인원 : 5인 - 손원용, 오상수, 김기영, 권형주, 이준호   
       
_Step 1_ ( ~2월 16일 )      
- 자료 조사 (3명) : 김기영, 권형주, 이준호   
- 데이터 → Cloud (2명) : 손원용, 오상수   

_Step 1-1_ (2월 16일 1차 발표 )   
- 발표 내용 : 데이터 자료 조사 후 자료에 대한 설명 및 과정 진척도 발표   

_Step 2_ (~2월 19일 전후 )   
- 팀원 모두 참가하여 데이터 전처리 수행   
- 데이터 처리 방식에 따라 알고리즘 분석에 대한 고민도 함께 해야함   

_Step 2-2_ (2월 19일 2차 발표 )   
- 발표 내용 : 데이터 전처리 방식에 대한 전반적인 프로세스 소개, 덜 되었더라도 경과에 대한 설명도 괜찮음   

_Step 3_ ( Step 2 이후 ~ 2월 26일 )   
- 알고리즘 분석이 완료되는대로 학습 수행 및 결과 확인 → 결과 분석 및 정확도 향상 (반복작업 수행)   
  ※ 알고리즘 조사 (회귀, 시계열, 딥러닝 LSTM, (구글, 페이스북) forecast, etc ...)   
  
_Step 3-2_ (2월 26일 최종 발표 )   
- 전반적인 과정에 대한 워크플로우 및 시각화된 내용을 토대로 발표 진행 (학회에 발표한다는 마인드로 PPT 준비)   


#### ※ 해야 할 작업   
(전체)   
트렐로 및 Github를 활용   
   시각화에 뛰어난 트렐로는 계획 관리 및 수행 과정 확인   
   Github로는 데이터 업로드 및 코드 공유   
   트렐로와 Github간의 하이퍼링크를 서로 달아서 시간 소요 최대한 감축   
(PPT)   
정리된 자료는 바로바로 개인적으로 저장한 후에 트렐로에 1차적으로 올리고 취합하여 github에 업로드(가 목표)   
(Step 1)   
자료조사(3인), 데이터 전송(2인) 모두 각자 소규모 팀 내에서 보고 있는 자료에 대해 겹치게 공부하지 않도록 사이트를 공유할 수 있으면 좋음   

※ 참고 사항   
이미지 업로드 과정에 대한 선생님 생각: dicom > 이미지 > tf.record > MongoDB(tf.record가 바로 안들어가면 csv or json or numpy 등을 활용)   
tf.record : 클라우드 스토리지에 넣으면 유연하게 처리 가능할 것으로 예상은 하고 계심   
zip > 로컬에 다시 풀면 300GB 넘음 (여유있게 350GB 필요) → 이에 대한 고민이 필요함.   

#### 26일 중간 결과
+ PPTX (나눔스퀘어, Noto Sans)
[PPT최종_210226.pptx](https://github.com/X-Ray-Project/main/files/6047455/PPT._210226.pptx)
+ PDF
[PPT최종_210226.pdf](https://github.com/X-Ray-Project/main/files/6047463/PPT._210226.pdf)

#### 이후 계획 요약(~3월 31일)
  : 각자 공부 중인 모델 학습 및 submission
  + EfficientDet
  + DETR
  + DetectoRS_ResNet
