import sys

#import thosttraderapi  as api
import random
from openctp_ctp import thosttraderapi as api
from openctp_ctp import mdapi


class CMdAuthSpiImpl (api.CThostFtdcTraderSpi,mdapi.CThostFtdcMdSpi):
    def __init__(self, tdapi,mdapi):
        super().__init__()
        self.tdapi = tdapi
        self.md_api = mdapi
    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("OnFrontConnected")
        req = api.CThostFtdcReqAuthenticateField()
        req.BrokerID = brokerid
        req.UserID = user
        req.AppID = appid
        req.AuthCode = authcode
        self.tdapi.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("OnFrontDisconnected: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: api.CThostFtdcRspAuthenticateField,
                          pRspInfo: api.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo is not None:
            print(f"OnRspAuthenticate: ErrorID={pRspInfo.ErrorID}, ErrorMsg={pRspInfo.ErrorMsg}")

        if pRspInfo is None or pRspInfo.ErrorID == 0:
            req = api.CThostFtdcReqUserLoginField()
            req.BrokerID = brokerid
            req.UserID = user
            req.Password = password
            req.UserProductInfo = "openctp"
            self.tdapi.ReqUserLogin(req, 0)