import sqlite3
conn = sqlite3.connect('aicaptrack.db')
cur = conn.cursor()
try:
    cur.execute('SELECT COUNT(*) FROM ai_capabilities')
    print('Records:', cur.fetchone()[0])
except Exception as e:
    print('Error:', e)
conn.close()
