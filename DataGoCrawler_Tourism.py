import os
import sys
import urllib.request
import datetime
import time
import json
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc

def get_request_url(url) :
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() ==200:
            print("[%s] Url Request Success" %datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error of URL : %s" %(datetime.datetime.now(), url))
        return None

def getNatVisitor(yyyymm, nat_cd, ed_cd) :
    end_point ='http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList'

    parameters ="?_type=json&serviceKey="+"tbVc2gJB%2FYUJTc8K6Gsildexx3mIqp5jAyds%2FJtCJxQJVQpEmaKKu7N82rM2DMJ3sDi6SVenibjmB7Ng8diMGQ%3D%3D"
    parameters +="&YM="+yyyymm
    parameters +="&NAT_CD="+nat_cd
    parameters +="&ED_CD="+ed_cd

    url = end_point + parameters
    retData = get_request_url(url)

    if (retData ==None) :
        return None
    else:
        return json.loads(retData)

def main():
    jsonResult = []
    national_code = "130"
    ed_cd = "E"

    nStartYear = 2017
    nEndYear = 2020

    for year in range(nStartYear, nEndYear) :
        for month in range(1,13):
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getNatVisitor(yyyymm, national_code, ed_cd)
            msg = jsonData['response']['header']['resultMsg']

            if(msg):                  
                try :
                    print(jsonData['response']['body'])
                    krName = jsonData['response']['body']['items']['item']['natKorNm']
                    krName = krName.replace(' ', '')

                except :
                    continue
        
                iTotalVisit = jsonData['response']['body']['items']['item']['num']
                print('%s_%s : %s' %(krName, yyyymm, iTotalVisit))
                jsonResult.append({'nat_name' : krName, 'nat_cd' : national_code, 'yyyymm':yyyymm, 'visit_cnt': iTotalVisit})
                cnVisit = []
                VisitYM = []
                index = []
                i = 0

        for item in jsonResult :
            index.append(i)
            cnVisit.append(item['visit_cnt'])
            VisitYM.append(item['yyyymm'])
            i = i+1
               

    with open('%s(%s)_해외방문객정보_%d_%d.json' % (krName, national_code,nStartYear, nEndYear-1), 'w', encoding = 'utf8') as outfile:
        retJson = json.dumps(jsonResult, indent =4, sort_keys = True, ensure_ascii =False)
        outfile.write(retJson)
        font_location = "c:/Windows/fonts/malgun.ttf"
        font_name = font_manager.FontProperties(fname=font_location).get_name()
        matplotlib.rc('font', family = font_name)
        plt.xticks(index, VisitYM)
        plt.plot(index, cnVisit)

        plt.xlabel('방문월')
        plt.ylabel('방문객수')
        plt.grid(True)
        plt.show()

if __name__ == '__main__' :
    main()
