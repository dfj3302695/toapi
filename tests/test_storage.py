import os
import time
from toapi.storage import Storage
from toapi.settings import Settings

html = """
<span class="RichText CopyrightRichText-richText" itemprop="text" data-reactid="128">
说明贪图安逸，厌恶不确定性，没有好奇心与冒险主义精神，在自由市场是永远发不了财的，即使PhD也不行。 
当我看懂今日头条的时候，其已经是可以和BAT放在一起讨论的了。但我甚至从来没有用过这个App。 
知乎作为人均年薪百万的社区，姿势水平应该是很高的了，一路唱衰BTC，价格却反而一路涨。
</span>
"""
url = "https://www.zhihu.com"


def test_disk_storage():
    Settings.storage["EXPIRATION"] = None
    store = Storage(Settings)
    store.save(url, html)
    assert store.get(url) == html


def test_db_storage():
    basedir = os.path.abspath(os.path.dirname(__file__))
    Settings.storage.update({
        "DB_URL": "sqlite:///" + os.path.join(basedir, 'data.sqlite'),
        "EXPIRATION": 5
    })
    store = Storage(Settings)
    store.save(url, html)
    assert store.get(url) == html


def test_disk_expiration():
    Settings.storage["EXPIRATION"] = 5
    store = Storage(Settings)
    store.save(url, html)
    time.sleep(6)
    assert store.get(url) is None


def test_db_expiration():

    basedir = os.path.abspath(os.path.dirname(__file__))
    Settings.storage.update({
        "DB_URL": "sqlite:///" + os.path.join(basedir, 'data.sqlite'),
        "EXPIRATION": 5
    })
    store = Storage(Settings)
    store.save(url, html)
    time.sleep(6)
    assert store.get(url) is None
