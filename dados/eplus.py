import pandas as pd
import sqlite3

conn   = sqlite3.connect('eplusout.sql')

df = pd.read_sql("""
SELECT t.SimulationDays, t.Hour, t.Minute, rd.Value
FROM ReportData rd
    LEFT JOIN Time t ON (rd.TimeIndex == t.TimeIndex)
WHERE t.WarmupFlag == 0
""", conn)

print(df.head(2))
