import copy


class OneMinuteTick:
    OneMinuteDic = {
        "InstrumentID": "",
        "UpdateTime": "99:99:99",
        "UpdateMinute": "99:99",
        "LastPrice": 9999999.00,
        "HighPrice": 0.00,
        "LowPrice": 0.00,
        "OpenPrice": 0.00,
        "PreSettlementPrice": 0.00,
        "PreClosePrice": 0.00,
        "TickVolume": 0,
        "Volume": 0,
        "TickTurnover": 0.00,
        "Turnover": 0.00,
        "OpenInterest": 0,
        "PreOpenInterest": 0,
        "MinusInterest": 0,
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
                                                              :-2]) and pDepthMarketData.UpdateTime != '21:00:00'

        self.bar_dict[pDepthMarketData.InstrumentID]["UpdateMinute"] = pDepthMarketData.UpdateTime[:-2]
        self.bar_dict[pDepthMarketData.InstrumentID]["UpdateTime"] = pDepthMarketData.UpdateTime
        if is_new_1minute:
            if last_update_time == "99:99:99":
                self.bar_dict[pDepthMarketData.InstrumentID]["Volume"] = 0
                self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"] = 0.00
            else:
                self.bar_dict[pDepthMarketData.InstrumentID]["Volume"] = pDepthMarketData.Volume - \
                                                                         self.bar_dict[pDepthMarketData.InstrumentID][
                                                                             "TickVolume"]
                self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"] = pDepthMarketData.Turnover - \
                                                                           self.bar_dict[pDepthMarketData.InstrumentID][
                                                                               "TickTurnover"]
            self.bar_dict[pDepthMarketData.InstrumentID]["TickVolume"] = pDepthMarketData.Volume
            self.bar_dict[pDepthMarketData.InstrumentID]["TickTurnover"] = pDepthMarketData.Turnover
        else:
            self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"] = pDepthMarketData.LastPrice
            self.bar_dict[pDepthMarketData.InstrumentID]["Volume"] += pDepthMarketData.Volume - \
                                                                      self.bar_dict[pDepthMarketData.InstrumentID][
                                                                          "TickVolume"]
            self.bar_dict[pDepthMarketData.InstrumentID]["TickVolume"] = pDepthMarketData.Volume
            self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"] += pDepthMarketData.Turnover - \
                                                                        self.bar_dict[pDepthMarketData.InstrumentID][
                                                                            "TickTurnover"]
            self.bar_dict[pDepthMarketData.InstrumentID]["TickTurnover"] = pDepthMarketData.Turnover
            self.bar_dict[pDepthMarketData.InstrumentID]["OpenInterest"] = pDepthMarketData.OpenInterest
            self.bar_dict[pDepthMarketData.InstrumentID]["PreOpenInterest"] = pDepthMarketData.PreOpenInterest
            self.bar_dict[pDepthMarketData.InstrumentID]["MinusInterest"] = pDepthMarketData.OpenInterest - pDepthMarketData.PreOpenInterest
            self.bar_dict[pDepthMarketData.InstrumentID]["PreSettlementPrice"] = pDepthMarketData.PreSettlementPrice
            self.bar_dict[pDepthMarketData.InstrumentID]["PreClosePrice"] = pDepthMarketData.PreClosePrice
            if self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] <= pDepthMarketData.LastPrice:
                self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"] = pDepthMarketData.LastPrice
            if self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] >= pDepthMarketData.LastPrice:
                self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] = pDepthMarketData.LastPrice
            self.bar_dict[pDepthMarketData.InstrumentID]["OpenPrice"] = pDepthMarketData.OpenPrice

            sql = "insert into QUANT_FUTURE_MD_ONEMIN (TRADINGDAY,INSTRUMENTID,LASTPRICE,HIGHESTPRICE,LOWESTPRICE,PRESETTLEMENTPRICE" \
                  ",PRECLOSEPRICE,PREOPENINTEREST,OPENPRICE,VOLUME,TURNOVER,OPENINTEREST" \
                  ",UPDATETIME,UPDATEMINUTE,UPRATIO,INTERESTMINUS,INTERESTRATIO)values(" \
                  "'" + pDepthMarketData.TradingDay + "','" + self.bar_dict[pDepthMarketData.InstrumentID]["InstrumentID"] + \
                  "'," + str(self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"]) + \
                  "," + self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"] + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["PreSettlementPrice"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["PreClosePrice"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["PreOpenInterest"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["OpenPrice"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["Volume"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["OpenInterest"]) + \
                  ",'" + self.bar_dict[pDepthMarketData.InstrumentID]["UpdateTime"] + \
                  "','" + self.bar_dict[pDepthMarketData.InstrumentID]["UpdateMinute"] + \
                  "'," + str(( self.bar_dict[pDepthMarketData.InstrumentID]["LastPrice"] - self.bar_dict[pDepthMarketData.InstrumentID]["PreSettlementPrice"]) / self.bar_dict[pDepthMarketData.InstrumentID]["PreSettlementPrice"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["MinusInterest"]) + \
                  "," + str(self.bar_dict[pDepthMarketData.InstrumentID]["MinusInterest"]/self.bar_dict[pDepthMarketData.InstrumentID]["PreOpenInterest"]) + ")"

        print("sqlstr is:"+sql)
        '''
        print("last time is:" + last_update_time + ",is_new_1minute is:" + str(
            is_new_1minute) + ",Instrument is:" + pDepthMarketData.InstrumentID +
              ",LastPrice is:" + str(pDepthMarketData.LastPrice) + ", high price is:" + str(
            self.bar_dict[pDepthMarketData.InstrumentID]["HighPrice"]) +
              ",OpenPrice is:" + str(self.bar_dict[pDepthMarketData.InstrumentID]["OpenPrice"]) + ",LowPrice is:" + str(
            self.bar_dict[pDepthMarketData.InstrumentID]["LowPrice"]) +
              ",volume is:" + str(self.bar_dict[pDepthMarketData.InstrumentID]["Volume"]) + ",turnover is:" + str(
            self.bar_dict[pDepthMarketData.InstrumentID]["Turnover"]) +
              ",MinusInterest is:" + str(self.bar_dict[pDepthMarketData.InstrumentID]["MinusInterest"]))
        '''
