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

    def __init__(self, InstrumentID):
        self.OneMinuteDic["InstrumentID"] = InstrumentID
        print("hello:"+InstrumentID)
