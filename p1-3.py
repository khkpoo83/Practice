# **문제 1-3: 다가오는 이벤트 찾기**

# `events.json` 파일을 읽어서:
# 1. 오늘 날짜 기준으로 7일 이내에 있는 이벤트만 필터링
# 2. 각 이벤트에 D-Day 정보를 추가 (예: "D-3", "D-Day", "D+2")
# 3. D-Day가 가까운 순서로 정렬
# 4. 결과를 `upcoming_events.json`에 저장

# **힌트:**
# - 이미 지난 이벤트는 제외
# - "D-Day"는 오늘, "D-1"은 내일, "D+1"은 어제

# datetime, timedelta usage.....
# now=datetime.now()
# print(now.ctime())
# print(now)
# print(now.isoformat())
# print(now.strftime('%Y-%m-%d %H:%M:%S'))
# dstr='2026-01-13 17:30:34'
# ddate=datetime.strptime(dstr,'%Y-%m-%d %H:%M:%S')
# print(ddate,type(ddate))
# print(now, now+timedelta(days=1))

from datetime import datetime, timedelta
import json
# {'title': '프로젝트 마감', 'date': '2026-01-15', 'description': 'Q1 프로젝트 최종 제출'}
# {'title': '팀 회식', 'date': '2026-01-18', 'description': '신년 회식'}
# {'title': '고객 미팅', 'date': '2026-01-14', 'description': '신규 고객사 미팅'}
# {'title': '개발자 컨퍼런스', 'date': '2026-01-25', 'description': '연례 개발자 행사'}
# {'title': '시스템 점검', 'date': '2026-01-10', 'description': '서버 정기 점검 (이미 지남)'}
# {'title': '교육 세미나', 'date': '2026-01-16', 'description': '신입 교육'}
# {'title': '프레젠테이션', 'date': '2026-01-19', 'description': '임원진 보고'}
# {'title': '분기 워크샵', 'date': '2026-02-05', 'description': '1분기 워크샵'}
# {'title': '성과 평가', 'date': '2026-01-13', 'description': '연말 성과 평가 (오늘)'}
with open('./Resource/events.json','rt',encoding='utf-8') as f:
    targets=[]
    rst=json.load(f)
    for r in rst:
        target={}
        dday=datetime.strptime(r['date'],'%Y-%m-%d')
        # print(datetime.now()+timedelta(days=-7),datetime.now()-timedelta(days=-7))
        # print(dday,datetime.now()+timedelta(days=-7), datetime.now()-timedelta(days=-7))
        if dday > datetime.now()+timedelta(days=-7) and  dday < datetime.now()-timedelta(days=-7):
            if (datetime.now()-dday).days ==0:
                r['gap']='D-Day'
            elif (datetime.now()-dday).days > 0:
                r['gap']='D+'+str((datetime.now()-dday).days)
            else:
                r['gap']='D'+str((datetime.now()-dday).days)
            print(lambda x:0 if r['gap'][2:]=='Day' else int(r['gap'][1:]))
            targets.append(r)
    for i in targets:
        print(i)
    print('-'*100)
    sorted_targets=sorted(targets,key=lambda x:0 if x['gap'][2:]=='Day' else int(x['gap'][2:]))
    for i in sorted_targets:
        print(i)

with open('./Resource/upcoming_events.json','wt',encoding='UTF-8') as f:
    json.dump(sorted_targets,f,ensure_ascii=False,indent=2)