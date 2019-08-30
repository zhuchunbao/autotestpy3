#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests, time, re
import urllib
import pymysql
import json
#import ifconfig
HOSTNAME = '127.0.0.1'
def test_readSQLcase():
    sql="SELECT id,`apiname`,apiurl,apimethod,apiparamvalue,apiresult,`apistatus` from apitest_apis "
    coon =pymysql.connect(user='zhdbuser',passwd='zhdbuser123',db='autotest',port=3306,host='10.30.50.167',charset='utf8')
    cursor = coon.cursor()
    aa=cursor.execute(sql)
    info = cursor.fetchmany(aa)
    print (info)
    for ii in info:
        case_list = []
        case_list.append(ii)
        interfaceTest(case_list)
        coon.commit()
        cursor.close()
        coon.close()
def interfaceTest(case_list):
    res_flags = []
    request_urls = []
    responses = []
    strinfo = re.compile('{seturl}')
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[1]
            method = case[3]
            url = case[2]
            param = case[4]
            print(param)
            res_check = case[5]
        except Exception as e:
            return '测试用例格式不正确！ %s'%e
        if param== '':
            new_url = 'http://'+'api.test.com.cn'+url
        elif param== 'null':
            url = strinfo.sub(str(seturl('seturl')),url)
            new_url = 'http://'+ url
        else:
            #拼接请求地址
            url = str(seturl('seturl'))+str(url)
            new_url = url
            request_urls.append(new_url)
        if method.upper() == 'GET':
            headers = {'Authorization':'', 'Content-Type': 'application/json' }
            if "=" in urlParam(param):
                data = None
                print (str(case_id)+' request is get' +new_url.encode('utf-8')+'?'+urlParam(param).encode('utf-8'))
                results = requests.get(new_url+'?'+urlParam(param),data,headers=headers).text
                print(' response is get'+results.encode('utf-8'))
                responses.append(results)
                res = readRes(results,'')
            else:
                print('request is get ' +new_url+' body is '+urlParam(param))
                data = None
                req = urllib.request.Request(url=new_url,data=data,headers=headers,method="GET")
                try:
                    results = urllib.request.urlopen(req).read()
                    print (' response is get ')
                    print(results)
                except Exception as e:
                    return writeResult(case_id,'0')
                res = readRes(results,res_check)
                if 'pass' == res:
                    res_flags.append('pass')
                    writeResult(case_id,'1')

                else:
                    res_flags.append('fail')
                    writeResult(case_id,'0')

        if method.upper()=='PUT':
            headers = {'Host':HOSTNAME, 'Connection':'keep-alive', 'CredentialId':id, 'Content-Type':'application/json'}
            body_data=param
            results = requests.put(url=url,data=body_data,headers=headers)
            responses.append(results)
            res = readRes(results,res_check)
            if 'pass' == res:
                writeResult(case_id,'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id,'fail')
        if method.upper()=="PATCH":
            headers = {'Authorization':'Credential '+id, 'Content-Type': 'application/json' }
            data = None
            results = requests.patch(new_url+'?'+urlParam(param),data,headers=headers).text
            responses.append(results)
            res = readRes(results,res_check)
            if 'pass' == res:
                writeResult(case_id,'pass')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id,'fail')

        if method.upper()=="1":
            headers = {'Authorization':'Credential ', 'Content-Type': 'application/json' }
            if "=" in urlParam(param):
                data = None
                results = requests.patch(new_url+'?'+urlParam(param),data,headers=headers).text
                print (' response is post'+results.encode('utf-8'))
                responses.append(results)
                res = readRes(results,'')
            else:
                #print (str(case_id)+' request is ' +str(new_url)+' body is'+str(urlParam(param)).encode('utf-8'))
                results = requests.post(new_url,data=urlParam(param).encode('utf-8'),headers=headers).text
                print(results.encode('utf-8'))
                responses.append(results)
                res = readRes(results,res_check)
            if 'pass' == res:
                writeResult(case_id,'1')
                res_flags.append('pass')
            else:
                res_flags.append('fail')
                writeResult(case_id,'0')

def readRes(res,res_check):
    res = res.replace('":"',"=").replace('":',"=")
    print(res)
    res_check = res_check.split(';')
    print(res_check)
    for s in res_check:
        if s in res:
            pass
        else:
            return '错误，返回参数和预期结果不一致'+s
    return 'pass'
def urlParam(param):
    param1=param.replace('&quot;','"')
    return param1
def CredentialId():
    global id
    url = 'http://'+'api.test.com.cn'+'/api/Security/Authentication/Signin/web'
    body_data= json.dumps({"Identity":'test',"Password":'test'})
    headers = { 'Connection':'keep-alive','Content-Type': 'application/json'}
    response = requests.post(url=url,data=body_data,headers=headers)
    data=response.text
    regx = '.*"CredentialId":"(.*)","Scene"'
    pm = re.search(regx, data)
    id = pm.group(1)
def seturl(set):
    global setvalue
    sql = "SELECT `setname`,`setvalue` from set_set"
    coon =pymysql.connect(user='zhdbuser',passwd='zhdbuser123',db='autotest',port=3306,host='10.30.50.167',charset='utf8')
    cursor = coon.cursor()
    aa=cursor.execute(sql)
    info = cursor.fetchmany(aa)
    #print (info)
    coon.commit()
    cursor.close()
    coon.close()
    if info[0][0] == set:
        setvalue = info[0][1]
        print (setvalue)
    return setvalue
# def writeResult(case_id,result):
#     result = result.encode('utf-8')
#     now = time.strftime("%Y-%m-%d %H:%M:%S")
#     sql = "UPDATE apitest_apistep set apitest_apistep.apistatus=%s,apitest_apistep.create_time=%s where apitest_apistep.id=%s;"
#     param = (result,now,case_id)
#     print ('api autotest result is '+result.decode())
#     coon =pymysql.connect(user='root',passwd='test123456',db='autotest',port=3306,host='10.30.50.167',charset='utf8')
#     cursor = coon.cursor()
#     cursor.execute(sql,param)
#     coon.commit()
#     cursor.close()
#     coon.close()
def writeResult(case_id,result):
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "UPDATE apitest_apis set apitest_apis.apistatus=%s,apitest_apis.create_time=%s where apitest_apis.id=%s;"
    param = (result,now,case_id)
    print ('api autotest result is '+result.decode())
    coon =pymysql.connect(user='zhdbuser',passwd='zhdbuser123',db='autotest',port=3306,host='10.30.50.167',charset='utf8')
    cursor = coon.cursor()
    cursor.execute(sql,param)
    coon.commit()
    cursor.close()
    coon.close()
# def writeBug(bug_id,interface_name,request,response,res_check):
#     interface_name = interface_name.encode('utf-8')
#     res_check = res_check.encode('utf-8')
#     request = request.encode('utf-8')
#     now = time.strftime("%Y-%m-%d %H:%M:%S")
#     bugname = str(bug_id)+ '_' + interface_name.decode() + '_出错了'
#     bugdetail = '[请求数据]<br />'+request.decode()+'<br/>'+'[预期结
#     果]<br/>'+res_check.decode()+'<br/>'+'<br/>'+'[响应数据]<br />'+'<br/>'+response.decode()
#     print (bugdetail)
#     sql = "INSERT INTO `bug_bug` ("\
#     "`bugname`,`bugdetail`,`bugstatus`,`buglevel`, `bugcreater`,
#     `bugassign`,`created_time`,`Product_id`) "\
#     "VALUES ('%s','%s','1','1','邹辉', '邹辉', '%s',
#     '2');"%(bugname,pymysql.escape_string(bugdetail),now)
#     coon =
#     pymysql.connect(user='root',passwd='test123456',db='autotest',port=3306,host='127.0.0.1',charset='utf8
#     ')
#     cursor = coon.cursor()
#     cursor.execute(sql)
#     coon.commit()
#     cursor.close()
#     coon.close()
if __name__ == '__main__':
    test_readSQLcase()
    print ('Done!')
    time.sleep(1)