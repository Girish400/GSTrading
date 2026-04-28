import asyncio
import argparse
import ib_insync as ibi
import numpy as np
import time
import datetime
import math

class MarketDataApp:
    
    def __init__(self, TickerList, Port, ClientId):
        self.TickerList = TickerList
        self.Port = Port
        self.ClientId = ClientId        
        self.ib = ibi.IB()
        self.queue = asyncio.Queue()
        self.tickerdict = {}
        self.start_time = time.time()
        self.initial_Stock_Volume ={} 
        self.stocksenttoapp=[]


    def iterate_from_last(self,arr,volumearr):
        arr = arr[-600:] 
        for i in np.arange(arr.size-1, -1, -1):

            if round(arr[-1] - arr[i],2) >= 0.3:                   ## Price has increased from point A to point B by atleast 30 cents
                if len(arr) >=4:                                   ## Atleast 4 ticks 
                    if (volumearr[-1]-volumearr[0])*100 >= 50000:  ## While price is increased by 30 cents it should have 50K volume
                        return i       
        
            if round(arr[i] - arr[-1],2) >= 0.3:                   ## Price has Decreased from point A to point B by atleast 30 cents
                if len(arr) >=4:                                   ## Atleast 4 ticks 
                    if (volumearr[-1]-volumearr[0])*100 >= 50000:  ## While price is decreased by 30 cents it should have 50K volume
                        return i
        return -1


    def calculate_tick_percentage(self,arr):
        diff = np.unique(np.diff(arr), axis=0)
        up_ticks = np.sum(diff > 0) 
        down_ticks = np.sum(diff < 0) 
        total_ticks = len(diff)  
        up_tick_percentage = up_ticks / total_ticks * 100  
        down_tick_percentage = down_ticks / total_ticks * 100  
        return up_tick_percentage, down_tick_percentage


    def find_up_down_Percentage(self,arr,tickersymbol):
        volumearr = arr[:, 1]
        pricearr = arr[:, 0]
        eps = np.finfo(float).eps
        pricearr = pricearr[np.concatenate(([True], np.abs(np.diff(pricearr)) > eps))]
        pricearrindex = self.iterate_from_last(pricearr,volumearr)
        if pricearrindex > -1:
            up_percentage, down_percentage = self.calculate_tick_percentage(pricearr)
            if up_percentage == 100.00 or down_percentage == 100.00:
                print(f"Strategy 3  - For Symbol {tickersymbol} up ticks - {up_percentage:.2f}% , down ticks - {down_percentage:.2f}%  at {time.time()}")  


    async def ticker_handler(self):
        while True:
            ticker = await self.queue.get()   
            
            ## Calculate the Volume at Market Open on 9:30 EST
            if ticker.contract.symbol not in self.initial_Stock_Volume.keys():        
                if math.isnan(ticker.volume):
                    continue                        
                else:
                    self.initial_Stock_Volume[ticker.contract.symbol] = ticker.volume                
                    continue
            volume = (ticker.volume - self.initial_Stock_Volume[ticker.contract.symbol])
            
            currentdate = datetime.datetime.now()  
            
            
            try: 

                ## Strategy 1 - Big Ask / Big Bid at the Open
                if currentdate.hour == 6 and currentdate.minute == 30 and currentdate.second < 59: 
                    if (ticker.ask - ticker.bid) <= 0.03:
                        
                        if ticker.askSize >= 50000.0:
                            if ticker.contract.symbol not in self.stocksenttoapp:
                                self.stocksenttoapp.append(ticker.contract.symbol)
                                print(f"Strategy 1  - Big Ask for Symbol {ticker.contract.symbol} askSize {ticker.askSize} @ {currentdate}") 
                                self.queue.task_done()
                                return
                        
                        if ticker.bidSize >= 50000.0:
                            if ticker.contract.symbol not in self.stocksenttoapp:
                                self.stocksenttoapp.append(ticker.contract.symbol)
                                print(f"Strategy 1 - Big Bid for Symbol {ticker.contract.symbol} askSize {ticker.bidSize} @ {currentdate}") 
                                self.queue.task_done()
                                return
                

                ## Strategy 2 - One Minute ORB
                if currentdate.hour == 6 and currentdate.minute == 31 and currentdate.second <= 2:                           
                    if ticker.volume > 1000:                                                                                                            # 1.  Volume is greater than 100K in Pre-Market
                        if volume > 800:                                                                                                                # 2.  Volume is greater than 180K after Regular Market open 
                            if ticker.shortableShares > 100000:                                                                                         # 3.  Shortable Shares > 100K                        
                                if ticker.ask-ticker.bid < 0.03:                                                                                        # 4.  Spread <  6 cents                            
                                    if ticker.tradeRate > 1000:                                                                                         # 5.  Trade Rate > 1000
                                        if ticker.tradeCount > 1000:                                                                                    # 6.  Trade Count > 1000
                                            if ticker.volumeRate > 50000:                                                                              # 7.  Volume Rate > 100000
                                                if ticker.last > ticker.vwap:                                                                           # 8.  LTP > VWAP                                 
                                                    if ticker.last >  ticker.open:                                                                      # 9.  LTP > Open                                    
                                                        if ticker.last > ticker.close:                                                                  # 10.  LTP >= PCL                                        
                                                            if ticker.high-ticker.last < 0.11:                                                          # 11.  LTP closed near Day High                                            
                                                                if (ticker.last-ticker.open) > 0.24:                                                    # 12. One Minute Candle is Green
                                                                    if ticker.low < ticker.vwap:                                                        # 13. Day Low is below VWAP                                                   
                                                                       if ticker.contract.symbol not in self.stocksenttoapp:
                                                                            self.stocksenttoapp.append(ticker.contract.symbol)
                                                                            print(f"Strategy 2 - Orb up for Symbol {ticker.contract.symbol} at {currentdate} volumerate {ticker.volumeRate} tradecount {ticker.tradeCount} traderate {ticker.tradeRate}")
                                                                            self.queue.task_done()  
                                                                            return      
                                                else:                                                                                                   # 8.  LTP < VWAP                                 
                                                    if ticker.last <  ticker.open:                                                                      # 9.  LTP < Open
                                                        if ticker.last < ticker.close:                                                                  # 10.  LTP < PCL
                                                            if ticker.last-ticker.low <  0.11:                                                          # 11.  LTP closed near Day Low
                                                                if (ticker.open-ticker.last) >  0.24:                                                   # 12. One Minute Candle is Red
                                                                    if ticker.high > ticker.vwap:                                                       # 13. Day High is above VWAP
                                                                        if ticker.contract.symbol not in self.stocksenttoapp:
                                                                            self.stocksenttoapp.append(ticker.contract.symbol)
                                                                            print(f"Strategy 2 - Orb down for Symbol {ticker.contract.symbol} at {currentdate} volumerate {ticker.volumeRate} tradecount {ticker.tradeCount} traderate {ticker.tradeRate}")
                                                                            self.queue.task_done()
                                                                            return 
                
                ## Strategy 3 - Sudden Price Change of 40 cents with  minimum 100K Volume
                if ticker.ask - ticker.bid <= .03:
                    self.tickerdict[ticker.contract.symbol].append([round(((ticker.ask+ticker.bid)/2),2), ticker.volume])
                    self.find_up_down_Percentage(np.array(self.tickerdict[ticker.contract.symbol]),ticker.contract.symbol)
                    self.queue.task_done()
            except:
                print("Error in ticker_Handler:")


                        

    async def run(self):   
        tasks = []        
        with await self.ib.connectAsync(clientId=self.ClientId, port=self.Port):    
            for i in args.TickerList:
                self.tickerdict[i] = []    
            contracts = [ibi.Stock(symbol, 'SMART', 'USD') for symbol in self.TickerList]
            await self.ib.qualifyContractsAsync(*contracts)     
            self.ib.reqMarketDataType(3)         
            [self.ib.reqMktData(contract, '165,233,236,293,294,295',False, False) for contract in contracts]                    
            await asyncio.sleep(2)
            async for tickers in self.ib.pendingTickersEvent:
                [self.queue.put_nowait(ticker) for ticker in tickers]
                     
                        
    def stop(self):                 
        self.ib.disconnect()
        
              
async def main():    
    await asyncio.gather(*[app.run(), app.ticker_handler(), app.ticker_handler(), app.ticker_handler(), app.ticker_handler(), app.ticker_handler()])
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--TickerList', default=['SPY'], nargs='+')
    parser.add_argument('--Port', default=7497)
    parser.add_argument('--ClientId', default=101)
    args = parser.parse_args()
    app = MarketDataApp(args.TickerList, args.Port, args.ClientId)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("CTL+C Detected.Quitting!!")
    except Exception as e:
        print("Error in __main__:",e)
    finally:        
        app.stop()
