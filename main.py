import hashlib
import json
import re
import time

import requests

session = requests.session()


def getTimestamp():
    return str(round(time.time() * 1000))


def getsign(data):
    t = getTimestamp()
    return hashlib.md5(
        (_m_h5_tk.split('_')[0] + "&" + t + "&" + '24679788' + "&" + json.dumps(data)).encode()).hexdigest(), t


def sendCode(phone):
    global _m_h5_tk
    while True:
        try:
            url = 'https://acs.youku.com/h5/mtop.youku.dsp.right.verification/1.0/'
            data = {"phoneNum": phone}
            sign, t = getsign(data)
            req = {
                'jsv': '2.5.1',
                'appKey': '24679788',
                't': t,
                'sign': sign,
                'api': 'mtop.youku.dsp.right.verification',
                'v': '1.0',
                'type': 'jsonp',
                'dataType': 'jsonp',
                'timeout': '10000',
                'preventFallback': 'true',
                'callback': 'mtopjsonp2',
                'data': json.dumps(data)
            }
            response = session.get(url=url, headers=headers, params=req, timeout=20)
            res = response.text
            print(res)
            if '令牌过期' in res or '非法令牌' in res or '令牌为空' in res:
                cks = response.headers.get('Set-Cookie')
                if '_m_h5_tk=' in cks:
                    _m_h5_tk = re.findall('_m_h5_tk=(.*?);', cks)[0]
                    _m_h5_tk_enc = re.findall('_m_h5_tk_enc=(.*?);', cks)[0]
                    print(_m_h5_tk)
                    headers['Cookie'] = f'_m_h5_tk={_m_h5_tk};_m_h5_tk_enc={_m_h5_tk_enc};'
                    continue
            res = res.split("(")[1].replace(")", '')
            js = json.loads(res)
            return js['data']['model']['serialNumber']
        except Exception:
            return



def send(phone, code, serialNumber, rightCode):
    url = 'https://acs.youku.com/h5/mtop.youku.dsp.right.issue/1.0/'
    data = {"phoneNum": phone, "checkCode": code,
            "serialNumber": serialNumber,
            "rightCode": rightCode,
            "ua": "227!SSiSphDqgZnmkMAvUi9fRDudZ+P4JL9j4lPPOibZCSQWntR3FDoMExrUVgiE9O3aPEMwCSPE8mJMtS3Oe8xcJPWY6+o1wHRenHEueEHWji3cntkk+Vjh3SIb++TfrYvCn5ElOsvHa7Kzho78DxnL3XQWrmVXDWYiHXEPO6mCqjIXntjkHEn13DQWqmVXmzY9nh9uhfvgaCK+IojADWjK3X0jiQOXDppC7DjPD7UQaBMiHtR8DxHD3luZZRdPa/kht19ueEvHa7KzntkkDxnDQ9f1wZ+XDpvCnHEuOIPXaRKWjtRhlknLfi2WqKsHmppinXPPOJjXa7mHntkhS2ndfiNAqKCXDpABED4JOJjX7s1COQyxgV3tJRGuGAIKei9tBI7d5p7CD0HQcpwygES8J4HQ5K+CgsODrnPw5E+iy0HN3KphfZa0zmHHT4wa8J3rN8Uu7mGjc23L97BdktV7w3laK4lTlCC3bSY5IXsFSjkRLopbviCpcycUSl8P4ueYjL+VbuZEOsxZ1wT4PK+4SLr/REB7i/ctMkn+LpCQWXokv8PS+Qc+krfb1aIF4+v78fs3/vKrh2aJVIfaDDxC/wu8QL3x5twIgGCaIiE6prHrCwljJsntctxmLm+2J2ORykMFj1L4OaJxpk/zBBTLeObVB8oWGS9IQehPYGyXa1Xyp0CZiI/DYaL0InWGzN0OcK407EfPEd06p1wenjt0unZvr0BWBjdT7E8Hece6VpzySGdkQ1waCMje1cWHBd1vas3JJ9fPRwbSihvuv31EwXEmB7UdN1JeWExLybeGEt3D/MFbtYFk1CRSBCVtsxFXSvCXgqG5sWvfw2lNK1BvrgO0YpJdm1IkEPSs8x7PS4B1C/IcttQ/IZ+ydYGXbTVuL3IXpPozwn0b9I99AIQaPLaCGy21zFrJ4fwcYew/fvQY9BTHmyQQAUpKJcyALhID5/wDKkbpGT6zJ4IP7r1z1Jkx27fWVsyPAfgJKONo6RgeWJD/6likPyVX4KGbseE/AJPqsezKaHei7UpSZweCUTVtuzmCIEu9/swGCGm6vwKVOXkSGXT+TzCFxRE/uQ3fwnFpBSgCGrTAAPa3JwAK4cpLZizOQERAQamACmS84rhq/esoDuqk7EugjjZNK+sACd9C25h+DzKw5ftqvtWLEyNEn2N5lK4uq1dVHFCy7Ic2dJFJ7+YM8/OEjBpz2tleLsxxH961uEyX+qDcLwunKdbxucUmV0fDVbNFBCqzNHq8C38d8JcT7eVFz+lnf1OE58v55aF+pGdvcH9IHUZL07f0jr6G0E+eiN5LCqDgt/WXP09jnc8u",
            "umidToken": "GB5724D513AA53085C65289DA7DE30ABFD88B3F77D3B4202C5B"}
    sign, t = getsign(data)
    req = {
        'jsv': '2.5.1',
        'appKey': '24679788',
        't': t,
        'sign': sign,
        'api': 'mtop.youku.dsp.right.issue',
        'v': '1.0',
        'type': 'jsonp',
        'dataType': 'jsonp',
        'timeout': '10000',
        'preventFallback': 'true',
        'asac': '2A22A26ORIWKONH1LJQSQH',
        'callback': 'mtopjsonp2',
        'data': json.dumps(data)
    }
    res = session.get(url=url, headers=headers, params=req, timeout=20).text
    print(res)


def getYouKu1(phone):
    res = requests.get(f'http://fljd.tinghongzz.com/api/Welfare/YouKuDay?phone={phone}')
    print(res.text)


if __name__ == '__main__':
    print("")
    _m_h5_tk = '4a1e0d12586895e37b3ac2cf409049e9_1708537182166'

    headers = {
        "Cookie": ""
    }
    print("请输入手机号：")
    phone = input()

    codes = ['luckyz1lqj4opbrxbcpwpq', 'luckywveplro70oadf56v6', 'luckylbwp3ojbpypaulqzq']
    for it in codes:
        serialNumber = sendCode(phone)
        print("请输入验证码：")
        code = input()
        send(phone, code, serialNumber, it)
    getYouKu1(phone)
