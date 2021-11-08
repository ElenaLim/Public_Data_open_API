
import pandas as pd
import bar_chart_race as bcr

#csv파일 불러오기(코로나 전국 확진자)
corona_csv=pd.read_csv('corona_kr.csv')

#print(corona_csv.head(19))

## 각 컬럼 값 ## (포털 문서에서 꼭 확인하세요)
"""
SEQ : 게시글번호(국내 시도별 발생현황 고유값)
CREATE_DT: 	등록일시분초
DEATH_CNT: 	사망자 수
GUBUN: 	시도명(한글)
GUBUN_CN: 	시도명(중국어)
gubunEn: 시도명(영어)
INC_DEC: 전일대비 증감 수
ISOL_CLEAR_CNT: 격리 해제 수
QUR_RATE: 10만명당 발생률
STD_DAY: 기준일시
UPDATE_DT: 수정일시분초
DEF_CNT: 확진자 수
ISOL_ING_CNT: 격리중 환자수
OVER_FLOW_CNT: 해외유입 수
LOCAL_OCC_CNT: 지역발생 수

""" 

#필요한 데이터만 남기고 지우기
corona = corona_csv[['createDt','defCnt','gubunEn']] # 등록일시분초, 확진자 수, 시도명(영어)
#print(corona.head(19))

#열 순서 바꾸기 (등록일시, 시도명, 확진자 수 순)
corona = corona[['createDt','gubunEn','defCnt']]
#print(corona.head(19))

#필요없는 데이터 지우기(검역Lazaretto, 토탈Total)
condition = (corona.gubunEn != 'Lazaretto') & (corona.gubunEn !='Total')
corona = corona[condition]
#print(corona.head(17))

# 열값을 지역(gubunEn)으로, 값을 확진자 수(defCnt)로 하여 피봇팅하기
corona_df = corona.pivot_table(values = 'defCnt', index = ['createDt'], columns='gubunEn')

#nan값 있는지 확인 True이면 null값이 있음
#print(pd.isnull(corona_df))

# NaN값을 0으로 바꾸어 주기
corona_df.fillna(0,inplace=True)
#print(corona_df.head())

# 확진자 수 누적값으로 만들어주기
corona_df.iloc[:,0:-1] = corona_df.iloc[:,0:-1].cumsum()
print(corona_df.head())

#bar_chart_race로 시각화하기
bcr.bar_chart_race(df = corona_df,
                    n_bars= 17,
                    sort='desc',
                    title='Corona in Korea',
                    filename='한국_코로나확진자.mp4')
                  