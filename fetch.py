import datetime, time
import urllib2
from sqlalchemy import create_engine
from settings import SQLALCHEMY_DATABASE_URI

master_path = "/home/ross/nas/downloads"
delay = 3600

engine = create_engine('sqlite:///data/data.db')
conn = engine.connect()

def log(message):
    print "[%s] %s" % (datetime.datetime.now(), message)

while True:
    log("Checking for files")

    try:
        downloads = conn.execute("""SELECT * FROM downloads WHERE completed_at IS NULL AND started_at IS NULL AND download_at <= DATETIME('now')""").fetchall()

        for row in downloads:
            row = dict(row)

            conn.execute("""UPDATE downloads SET started_at = DATETIME('now') WHERE id = %d""" % row['id'])

            log("Downloading #%d %s" % (row['id'], row['url']))

            dst_name = row['url'].split('/')[-1]
            dst_path = master_path + '/' + dst_name

            log("Saving to %s" % dst_path)

            src = urllib2.urlopen(row['url'])
            with open(dst_path, 'wb') as dst:
                src_meta = src.info()
                src_size = int(src_meta.getheaders('Content-length')[0])
                log("Downloading %d bytes" % src_size)

                block_size = 8192
                while True:
                    buffer = src.read(block_size)
                    if not buffer:
                        break
                    dst.write(buffer)
            log("Finished downloading.")

            conn.execute("""UPDATE downloads SET completed_at = DATETIME('now') WHERE id = %d""" % row['id'])

    except Exception as e:
        log("ERROR %s: %s", (type(e), str(e)))
        exit()

    log("Waiting %d seconds..." % delay)
    time.sleep(delay)
