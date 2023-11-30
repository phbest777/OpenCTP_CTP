import copy


class OneMinuteTick:
    OneMinuteDic = {
        "InstrumentID": "",
        "UpdateTime": "99:99:99",
        "UpdateMinute": "99:99",
        "LastPrice": 0.00,
        "HighPrice": 0.00,
        "LowPrice": 0.0,
        "OpenPrice": 0.0,
        "TickVolume": 0,
        "Volume": 0,
        "TickTurnover": 0.0,
        "Turnover": 0.0,
        "OpenInterest": 0.0,
        "PreOpenInterest": 0.0,
        "MinusInterest": 0.0,
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
            # print("bar_dict is"+str(self.bar_dict[instrument_id]["LastPrice"]))

    def GetOneMinuteTick(self, pDepthMarketData):
        last_update_time = self.bar_dict[pDepthMarketData.InstrumentID]["UpdateTime"]
        is_new_1minute = (pDepthMarketData.UpdateTime[:-2] != last_update_time[
                                                              :-2]) and pDepthMarketData.UpdateTime != b'21:00:00'
        if is_new_1minute and last_update_time != "99:99:99":  # 新的一分钟开始数据分钟数据清0
            self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"] = 0.00
            self.bar_dict[pDepthMarketData.InstrumentID]["Volume"] = 0.00
            self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] = 0.00
            self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] = 0.00
            self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"]=0.00
        else:
            self.bar_dict[pDepthMarketData.InstrumentID]["UpdateMinute"] = pDepthMarketData.UpdateTime[:-2]
            self.bar_dict[pDepthMarketData.InstrumentID]["UpdateTime"] = pDepthMarketData.UpdateTime
            self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"] = pDepthMarketData.LastPrice
            self.bar_dict[pDepthMarketData.InstrumentID]["TickVolume"] = pDepthMarketData.Volume
            self.bar_dict[pDepthMarketData.InstrumentID]["Volume"] += pDepthMarketData.Volume - self.bar_dict[pDepthMarketData.InstrumentID]["TickVolume"]
            self.bar_dict[pDepthMarketData.InstrumentID]["TickTurnover"] =pDepthMarketData.Turnover
            self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"] += pDepthMarketData.Turnover-self.bar_dict[pDepthMarketData.InstrumentID]["TickTurnover"]
            self.bar_dict[pDepthMarketData.InstrumentID]["OpenInterest"]=pDepthMarketData.OpenInterest
            self.bar_dict[pDepthMarketData.InstrumentID]["PreOpenInterest"]=pDepthMarketData.PreOpenInterest
            self.bar_dict[pDepthMarketData.InstrumentID]["MinusInterest"]=pDepthMarketData.OpenInterest-pDepthMarketData.PreOpenInterest
        if self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] <= pDepthMarketData.LastPrice:
            self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] = pDepthMarketData.LastPrice
        if self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] >= pDepthMarketData.LastPrice:
            self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] = pDepthMarketData.LastPrice
        self.bar_dict[pDepthMarketData.InstrumentID]["OpenPrice"] = pDepthMarketData.OpenPrice
        if is_new_1minute and last_update_time != "99:99:99":
            for md_queue in self.md_queue_list:
                md_queue.put(copy.deepcopy(self.bar_dict[pDepthMarketData.InstrumentID]))
        # print(
        #    "is_new_1minute is:"+str(is_new_1minute)+",Instrument is:" + pDepthMarketData.InstrumentID + ",LastPrice is:" + str(pDepthMarketData.LastPrice) + ", high price is:" +
        #    str(self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"]))
