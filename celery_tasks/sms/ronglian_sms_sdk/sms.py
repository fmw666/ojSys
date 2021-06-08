from .SmsSDK import SmsSDK
from config import SMS_CONFIG


accId = SMS_CONFIG['accId']
accToken = SMS_CONFIG['accToken']
appId = SMS_CONFIG['appId']


def send_message(tid: str, mobile: str, datas: tuple):
    sdk = SmsSDK(accId, accToken, appId)

    resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)
