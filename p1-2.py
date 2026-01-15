# **문제 1-2: 매출 데이터 분석**

# `sales.csv` 파일을 읽어서:
# 1. 각 제품(product)별 총 매출액(price × quantity) 계산
# 2. 매출액이 높은 순서로 정렬
# 3. 상위 3개 제품을 `top_products.csv`에 저장 (컬럼: product, total_sales)
# 4. 전체 매출액 합계 출력

# **출력 예시:**
# ```
# 전체 매출액: 1,250,000원
# 상위 제품이 top_products.csv에 저장되었습니다.
# ```

# 풀이 2
# ai 풀이법. 통째로 딕셔너리로 만들어놓고, 변환해서 만들어내는 과정 주목
import csv
targets=[]
with open('./Resource/sales.csv','rt',encoding='utf-8') as f:
    rst=csv.DictReader(f,['product','price','quantity'])
    next(rst)
    target=dict()
    for r in rst:
        product=r['product']
        total_price=int(r['price'])*int(r['quantity'])

        if product not in target:
            target[product]=0
        target[product] +=total_price
    
    for k,v in target.items():
        targets.append({'product':k,'total_price':v})
        

    print('target::',target)
    print('targets::',targets)
    for i in targets:
        print(i)

# {'노트북': 14400000, 
#  '마우스': 1855000, 
#  '키보드': 1691000, 
#  '모니터': 5850000, 
#  '헤드셋': 750000, 
#  'USB메모리': 750000, 
#  '웹캠': 850000, 
#  '스피커': 612000, 
#  '태블릿': 3900000}

# 풀이 1 
# 같은 딕셔너리 객체를 리스트에 여러 번 추가 >>> 여기서 문제발생했었음..

import csv
with open('./Resource/sales.csv','rt',encoding='utf-8') as f:
    # target={}
    targets=[]
    category=set()
    rst=csv.DictReader(f,['product','price','quantity'])
    next(rst)
    for r1 in rst:
        category.add(r1['product'])
    f.seek(0,0)
    next(rst)
    for c1 in list(category):
        sum=0
        target={}
        # print("c1:",c1)
        for r2 in rst:
            # print(c1,r2)
            if c1 == r2['product']:
                sum+=int(r2['price'])*int(r2['quantity'])
                # print(c1,sum)
                target['product']=c1
                target['total_price']=sum
            else:
                continue
        targets.append(target)
        # print(target,type(target))
        f.seek(0,0)
        next(rst)
print('&'*100)
for r in targets:
    print(r)


   
