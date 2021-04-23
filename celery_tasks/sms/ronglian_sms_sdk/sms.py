from .SmsSDK import SmsSDK

accId = '8a216da878005a8001782111e32e0cb5'
accToken = '73464666c177436e9fffbf821aebf443'
appId = '8a216da878005a8001782111e4070cbc'


def send_message(tid: str, mobile: str, datas: tuple):
    sdk = SmsSDK(accId, accToken, appId)

    resp = sdk.sendMessage(tid, mobile, datas)
    # print(resp)
