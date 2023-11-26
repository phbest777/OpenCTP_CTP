"""
    交易demo - 订单录入
"""

from openctp_ctp import tdapi

td_fronts='tcp://180.168.146.187:10201'
td_front='tcp://180.168.146.187:10201'
user = '200231'
password = '777PHbest!!'
broker_id='9999'
authcode='0000000000000000'
appid='simnow_client_test'

class CTdSpiImpl(tdapi.CThostFtdcTraderSpi):
    """ 交易回调实现类 """

    def __init__(self, _api: tdapi.CThostFtdcTraderApi):
        super().__init__()
        self._api = _api

    def OnFrontConnected(self):
        """ 前置连接成功 """
        print("交易前置连接成功")

        # 认证请求
        req = tdapi.CThostFtdcReqAuthenticateField()
        req.BrokerID = broker_id
        req.UserID = user
        req.AppID = appid
        req.AuthCode = authcode
        self._api.ReqAuthenticate(req, 0)

    def OnFrontDisconnected(self, nReason: int):
        """ 前置断开 """
        print("交易前置连接断开: nReason=", nReason)

    def OnRspAuthenticate(self, pRspAuthenticateField: tdapi.CThostFtdcRspAuthenticateField,
                          pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 客户端认证应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("认证失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("认证成功")

        if pRspInfo is None or pRspInfo.ErrorID == 0:
            # 登录请求
            req = tdapi.CThostFtdcReqUserLoginField()
            req.BrokerID = broker_id
            req.UserID = user
            req.Password = password
            req.UserProductInfo = "openctp"
            self._api.ReqUserLogin(req, 0)

    def OnRspUserLogin(self, pRspUserLogin: tdapi.CThostFtdcRspUserLoginField,
                       pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 登录应答 """
        if pRspInfo and pRspInfo.ErrorID:
            print("登录失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg, "TradingDay=",
                  pRspUserLogin.TradingDay)
            return

        print("登录成功:", pRspUserLogin.UserID, "TradingDay=", pRspUserLogin.TradingDay)

        print("报单录入请求")

        # 请求市价单 或 限价单

        # 市价单
        self._api.ReqOrderInsert(market_order(), 0)
        # 限价单
        # self._api.ReqOrderInsert(limit_order(), 0)

    def OnRspOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField,
                         pRspInfo: tdapi.CThostFtdcRspInfoField, nRequestID: int, bIsLast: bool):
        """ 报单录入响应 """
        if pRspInfo and pRspInfo.ErrorID:
            print("报单录入失败: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)
            return

        print("报单录入成功")

    def OnRtnOrder(self, pOrder: tdapi.CThostFtdcOrderField):
        """ 报单回报 """
        print("报单回报:",
              "InstrumentID:", pOrder.InstrumentID,
              "ExchangeID:", pOrder.ExchangeID,
              "FrontID:", pOrder.FrontID,
              "SessionID:", pOrder.SessionID,
              "OrderRef:", pOrder.OrderRef,
              "OrderSysID:", pOrder.OrderSysID,
              "OrderPriceType:", pOrder.OrderPriceType,
              "Direction:", pOrder.Direction,
              "CombOffsetFlag:", pOrder.CombOffsetFlag,
              "LimitPrice:", pOrder.LimitPrice,
              "VolumeTotalOriginal:", pOrder.VolumeTotalOriginal,
              "OrderStatus:", pOrder.OrderStatus,
              "InsertDate:", pOrder.InsertDate,
              "InsertTime:", pOrder.InsertTime,
              )

    def OnErrRtnOrderInsert(self, pInputOrder: tdapi.CThostFtdcInputOrderField,
                            pRspInfo: tdapi.CThostFtdcRspInfoField):
        """报单录入错误回报"""
        if pRspInfo and pRspInfo.ErrorID:
            print("报单录入错误回报: ErrorID=", pRspInfo.ErrorID, "ErrorMsg=", pRspInfo.ErrorMsg)


def market_order():
    """市价单
    注意选择一个相对活跃的合约
    """
    req = tdapi.CThostFtdcInputOrderField()
    req.BrokerID = broker_id
    req.InvestorID = user
    req.ExchangeID = 'CZCE'
    req.InstrumentID = 'FG401'
    req.LimitPrice = 1670
    req.OrderPriceType = tdapi.THOST_FTDC_OPT_LimitPrice  # 价格类型市价单
    req.Direction = tdapi.THOST_FTDC_D_Buy  # 买
    req.CombOffsetFlag = tdapi.THOST_FTDC_OF_Open  # 开仓
    req.CombHedgeFlag = tdapi.THOST_FTDC_HF_Speculation
    req.VolumeTotalOriginal = 5
    req.IsAutoSuspend = 0
    req.IsSwapOrder = 0
    req.TimeCondition = tdapi.THOST_FTDC_TC_GFD
    req.VolumeCondition = tdapi.THOST_FTDC_VC_AV
    req.ContingentCondition = tdapi.THOST_FTDC_CC_Immediately
    req.ForceCloseReason = tdapi.THOST_FTDC_FCC_NotForceClose
    return req


def limit_order():
    """限价单
    注意选择一个相对活跃的合约及合适的价格
    """
    req = tdapi.CThostFtdcInputOrderField()
    req.BrokerID = broker_id
    req.InvestorID = user
    req.ExchangeID = 'CZCE'
    req.InstrumentID = 'SA401'  # 合约ID
    req.LimitPrice = 1841  # 价格
    req.OrderPriceType = tdapi.THOST_FTDC_OPT_LimitPrice  # 价格类型限价单
    req.Direction = tdapi.THOST_FTDC_D_Buy  # 买
    req.CombOffsetFlag = tdapi.THOST_FTDC_OF_Open  # 开仓
    req.CombHedgeFlag = tdapi.THOST_FTDC_HF_Speculation
    req.VolumeTotalOriginal = 7
    req.IsAutoSuspend = 0
    req.IsSwapOrder = 0
    req.TimeCondition = tdapi.THOST_FTDC_TC_GFD
    req.VolumeCondition = tdapi.THOST_FTDC_VC_AV
    req.ContingentCondition = tdapi.THOST_FTDC_CC_Immediately
    req.ForceCloseReason = tdapi.THOST_FTDC_FCC_NotForceClose
    return req


if __name__ == '__main__':
    # 实例化交易请求类
    api = tdapi.CThostFtdcTraderApi.CreateFtdcTraderApi("data\\trade\\"+user)  # type: tdapi.CThostFtdcTraderApi
    print("TTS交易API版本号:", api.GetApiVersion())
    print("交易前置:", td_front)
    # 实例化交易回调实现类
    spi = CTdSpiImpl(api)
    # 注册交易前置地址
    api.RegisterFront(td_front)
    # 交易请求实例 注册 交易回调实例
    api.RegisterSpi(spi)
    # 订阅私有流
    api.SubscribePrivateTopic(tdapi.THOST_TERT_QUICK)
    # 订阅公有流
    api.SubscribePublicTopic(tdapi.THOST_TERT_QUICK)
    # 初始化交易实例
    api.Init()

    # 阻塞 等待
    print("Press Enter key to exit ...")
    input()

    # 释放实例
    api.Release()