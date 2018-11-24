#coding:utf-8
'''
    author : linkin
    e-mail : yooleak@outlook.com
    date   : 2018-11-15
'''

import  asyncio
import aiohttp

url = "http://www.quanjing.com/creative/SearchCreative.aspx?id=7"

class a:
    def test(self):
        print(55555)


async def fetch(url):
    async with aiohttp.ClientSession() as s:
        async with s.get(url) as resp:
            r = await resp.text(encoding='utf-8')
            return r

async def run():
    res = await fetch(url)
    return {'result':res,'type':'response','spider':a()}

def done(future):
    future.result()['spider'].test()
    print('done,get :',future.result()['spider'].test())


# def callback(future):



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(run())
    task.add_done_callback(done)
    loop.run_until_complete(task)