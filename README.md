# MutualFundMonitor
This script when executed compares a list of user defined Mutual Fund NAV against the last recorded NAV

# Sample output
Downloaded [ mutual_funds.txt ] from https://www.amfiindia.com/spages/NAVAll.txt
Total no. of rows in file                 : 18164
Total no. of Mutual Funds entries in file : 15536


Fetching previously tracked Funds' details from file [ last_tracked_details.txt ]
Total no. of rows in file                 : 10
Total no. of Mutual Funds entries in file : 9

Fetched 9 records from previously tracked funds


 *** Comparing funds...
+------------------------------------------------------------------------------------+
| 0) Franklin India Ultra Short Bond Fund - Super Institutional - Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 27.585700
| 18-Oct-2019      : 34.895700
| Percent change   : -20.948140 %  (*)
+------------------------------------------------------------------------------------+
| 1) Aditya Birla Sun Life Tax Relief '96 - Growth Option
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 30.800000
| 18-Oct-2019      : 30.800000
| Percent change   : 0.000000 %
+------------------------------------------------------------------------------------+
| 2) Axis Long Term Equity Fund - Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 48.001200
| 18-Oct-2019      : 48.001200
| Percent change   : 0.000000 %
+------------------------------------------------------------------------------------+
| 3) Mirae Asset Emerging Bluechip Fund - Regular Plan - Growth Option
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 54.030000
| 18-Oct-2019      : 54.030000
| Percent change   : 0.000000 %
+------------------------------------------------------------------------------------+
| 4) Franklin India Prima Fund-Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 942.226700
| 18-Oct-2019      : 942.226700
| Percent change   : 0.000000 %
+------------------------------------------------------------------------------------+
| 5) Motilal Oswal Multicap 35 Fund (MOF35)-Regular Plan-Growth Option
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 26.701200
| 18-Oct-2019      : 26.701200
| Percent change   : 0.000000 %
+------------------------------------------------------------------------------------+
| 6) Tata Small Cap Fund-Regular Plan-Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 10.090300
| 18-Oct-2019      : 10.190300
| Percent change   : -0.981325 %
+------------------------------------------------------------------------------------+
| 7) HDFC Hybrid Equity Fund-Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 53.494000
| 18-Oct-2019      : 50.494000
| Percent change   : 5.941300 %  (*)
+------------------------------------------------------------------------------------+
| 8) Motilal Oswal Nasdaq 100 Fund of Fund- Regular Plan Growth
+------------------------------------------------------------------------------------+
| 18-Oct-2019      : 11.859300
| 18-Oct-2019      : 8.859300
| Percent change   : 33.862721 %  (*)

Dumping Monitored Funds details to file [ last_tracked_details.txt ]


+------------------------------------------------------------------------------------+
|                                 S T A T U S                                        |
+------------------------------------------------------------------------------------+
> Fund info not found  : id Equity Fund-Growth
> Fund info not found  : Mirae Asset Emerging
> Franklin India Ultra Short Bond Fund - Super Institutional - Growth  NAV changed from 34.895700 --> 27.585700
> HDFC Hybrid Equity Fund-Growth  NAV changed from 50.494000 --> 53.494000
> Motilal Oswal Nasdaq 100 Fund of Fund- Regular Plan Growth  NAV changed from 8.859300 --> 11.859300
