# **문제 1-1: 학생 성적 필터링**

# `students.json` 파일을 읽어서 다음을 수행하세요:
# 1. 평균 점수(math, english, science의 평균)가 80점 이상인 학생들만 필터링
# 2. 각 학생의 평균 점수를 새로운 필드로 추가
# 3. 결과를 `high_scores.json`에 저장
# 4. 조건을 만족하는 학생 수와 전체 평균 점수를 출력

# **출력 예시:**
# ```
# 고득점 학생 수: 3명
# 전체 평균: 85.67점

import json

total=0
cnt=0
targets=[]


def avg(kvarg):
    global cnt
    global total 
    average= round((kvarg['math']+kvarg['english']+kvarg['science'])/3,2)
    if average > 80:
        cnt+=1
        total+=kvarg['math']+kvarg['english']+kvarg['science']
        kvarg['avg']=average
        return kvarg


with open('./Resource/students.json','rt',encoding='utf-8') as f:
    rs=json.load(f)
    for r in rs:
        target=avg(r)
        if target:
            targets.append(target)

# for i in targets:
#     print(i)

with open('./Resource/high_socres.json','wt',encoding='utf-8') as f:
    rs=json.dump(targets,f,ensure_ascii=False)



print("대상자 : ",cnt,"명")
print("전체 평균: ",round(total/cnt/3,2),"점")


