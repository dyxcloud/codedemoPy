# encoding:utf-8

import base64
import time

import requests

'''
表格文字识别(异步接口)
'''


def get_token():
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    client_id = 'ak'
    client_secret = 'sk'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
    response = requests.get(host)
    if response:
        print(response.json())


'''
{'refresh_token': '25.7d1bfb04b689e375d028b0a7e6863e03.315360000.1954895806.282335-24508805', 'expires_in': 2592000, 'session_key': '9mzdAvDHRu1SNN4BuIH0Ys3rOO9GQZKTpOnpd3bT2gcJ1ijJ/aBr2xGZN8MHG/lzv29AqGsFvcphiQMJKEuYiZaZsfNUcw==', 'access_token': '24.92d90c7371ad8e9822051ff8634a7ab3.2592000.1642127806.282335-24508805', 'scope': 'public vis-ocr_ocr brain_ocr_scope brain_ocr_general brain_ocr_general_basic vis-ocr_business_license brain_ocr_webimage brain_all_scope brain_ocr_idcard brain_ocr_driving_license brain_ocr_vehicle_license vis-ocr_plate_number brain_solution brain_ocr_plate_number brain_ocr_accurate brain_ocr_accurate_basic brain_ocr_receipt brain_ocr_business_license brain_solution_iocr brain_qrcode brain_ocr_handwriting brain_ocr_passport brain_ocr_vat_invoice brain_numbers brain_ocr_business_card brain_ocr_train_ticket brain_ocr_taxi_receipt vis-ocr_household_register vis-ocr_vis-classify_birth_certificate vis-ocr_台湾通行证 vis-ocr_港澳通行证 vis-ocr_机动车购车发票识别 vis-ocr_机动车检验合格证识别 vis-ocr_车辆vin码识别 vis-ocr_定额发票识别 vis-ocr_保单识别 vis-ocr_机打发票识别 vis-ocr_行程单识别 brain_ocr_vin brain_ocr_quota_invoice brain_ocr_birth_certificate brain_ocr_household_register brain_ocr_HK_Macau_pass brain_ocr_taiwan_pass brain_ocr_vehicle_invoice brain_ocr_vehicle_certificate brain_ocr_air_ticket brain_ocr_invoice brain_ocr_insurance_doc brain_formula brain_ocr_facade brain_ocr_meter brain_doc_analysis brain_ocr_webimage_loc brain_ocr_doc_analysis_office brain_vat_invoice_verification wise_adapt lebo_resource_base lightservice_public hetu_basic lightcms_map_poi kaidian_kaidian ApsMisTest_Test权限 vis-classify_flower lpq_开放 cop_helloScope ApsMis_fangdi_permission smartapp_snsapi_base smartapp_mapp_dev_manage iop_autocar oauth_tp_app smartapp_smart_game_openapi oauth_sessionkey smartapp_swanid_verify smartapp_opensource_openapi smartapp_opensource_recapi fake_face_detect_开放Scope vis-ocr_虚拟人物助理 idl-video_虚拟人物助理 smartapp_component smartapp_search_plugin avatar_video_test b2b_tp_openapi b2b_tp_openapi_online', 'session_secret': '019bb5e5e11d653ad72b1a02d4cc5a1d'}
'''

access_token = '24.92d90c7371ad8e9822051ff8634a7ab3.2592000.1642127806.282335-24508805'


def send_file(file_path):
    send_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/request"
    # 二进制方式打开图片文件
    f = open(file_path, 'rb')
    img = base64.b64encode(f.read())
    params = {"image": img}
    send_url = send_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(send_url, data=params, headers=headers)
    if response:
        result = response.json()
        print(result)
        return result['result'][0]['request_id']


'''
{'result': [{'request_id': '24508805_2755772'}], 'log_id': 1625641864121170}
{'result': [{'request_id': '24508805_2755927'}], 'log_id': 1625643277344275}
'''


def get_result(result_id):
    send_url = "https://aip.baidubce.com/rest/2.0/solution/v1/form_ocr/get_request_result"
    send_url = send_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    params = {"request_id": result_id}
    response = requests.post(send_url, data=params, headers=headers)
    if response:
        result = response.json()
        print(result)
        return result['result']['result_data']

'''
{'result': {'result_data': 'http://bj.bcebos.com/v1/ai-edgecloud/177C3400C1974959908C6F8CD236B2E2.xls?authorization=bce-auth-v1%2Fd9272b4e9a38476db4470c2714e1339a%2F2021-07-07T07%3A11%3A13Z%2F172800%2F%2F975114f374a10374d46fe1d7ee4ba430a417b5a06e97f541a4be8dff7e2793a9', 'ret_msg': '已完成', 'request_id': '24508805_2755772', 'percent': 100, 'ret_code': 3}, 'log_id': 1625641946905180}
'''

if __name__ == '__main__':
    print('start')
    # get_token()
    my_file = r'D:\Download\OCR识别数据\2018302484249\SB000017845959_Ver1_100012\0001_结果.png'
    print("filepath: "+my_file)
    id = send_file(my_file)
    time.sleep(5)
    path = get_result(id)
    while ((path is None) or (len(path) == 0)):
        time.sleep(1)
        path = get_result(id)
    print("filepath: "+path)

