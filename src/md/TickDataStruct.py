class OneMinuteTick:
    OneMinuteDic = {
        "InstrumentID": "",
        "UpdateTime": "99:99:99",
        "LastPrice": 0.00,
        "HighPrice": 0.00,
        "LowPrice": 0.0,
        "OpenPrice": 0.0,
        "BarVolume": 0,
        "BarTurnover": 0.0,
        "BarSettlement": 0.0,
        "BVolume": 0,
        "SVolume": 0,
        "FVolume": 0,
        "DayVolume": 0,
        "DayTurnover": 0.0,
        "DaySettlement": 0.0,
        "OpenInterest": 0.0,
        "TradingDay": "99999999",
    }
    bar_dict = {}

    def __init__(self, instruments):
        '''
        self.OneMinuteDic["InstrumentID"] = pDepthMarketData.InstrumentID
        self.OneMinuteDic["UpdateTime"]=pDepthMarketData.UpdateTime
        self.OneMinuteDic["LastPrice"]=pDepthMarketData.LastPrice

        print("hello:"+pDepthMarketData.InstrumentID+",price is:"+pDepthMarketData.LastPrice+",high price is:"+)
        '''
        for instrument_id in instruments:
            # 初始化Bar字段
            self.OneMinuteDic["InstrumentID"] = instrument_id
            self.bar_dict[instrument_id] = self.OneMinuteDic.copy()
            #print("bar_dict is"+str(self.bar_dict[instrument_id]["LastPrice"]))

    def GetOneMinuteTick(self, pDepthMarketData):
        self.bar_dict[pDepthMarketData.InstrumentID]["UpdateTime"] = pDepthMarketData.UpdateTime
        self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"] = pDepthMarketData.LastPrice
        if self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] <= pDepthMarketData.LastPrice:
            self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] = pDepthMarketData.LastPrice
        print(
            "Instrument is:" + pDepthMarketData.InstrumentID + ",LastPrice is:" + str(pDepthMarketData.LastPrice) + ", high price is:" +
            str(self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"]))
