#!/usr/bin/env python
# pylint: disable=too-many-statements, line-too-long, W0703

"""
usage: pipenv run python httpserver.py 8000
"""

import csv
import io
import logging
import os
import sys
import time

from aiohttp import web
import aiofiles.os

routes = web.RouteTableDef()

@routes.get('/errorcheck.php')
async def errorcheck(_):
    """health check"""
    files = [
        'base_table.tar',
        'budget_control.tar',
        'targeting.csv',
        'targeting_bundle_rate.csv',
        'global_filter_list.csv',
        'ttl.tar',
    ]
    mtime = 0
    # 返回 files 所有文件中更新最早的一个文件时间（在 alerts 端，相当于所有文件中只要有一个不更新了，即会用最早的时间来判断报警）
    try:
        for file in files:
            stat = await aiofiles.os.stat(file)
            if mtime == 0 or stat.st_mtime < mtime:
                mtime = stat.st_mtime
    except Exception as error:
        logging.error('getmtime error: %s', error)
    return web.Response(text=f'{int(mtime):d}')


@routes.get('/budget_control_updated_time')
async def budget_control_updated_time(_):
    """budget_control_updated_time"""
    files = [
        'dsp_revenue.csv',
        'platform_cost.csv',
    ]
    updated_time = '1984-01-01T00:00:00'
    try:
        for filename in files:
            async with aiofiles.open(filename, mode='rb') as file:
                data = await file.read()
                for row in csv.DictReader(io.StringIO(data.decode()+'\n')):
                    if updated_time < row['update_time']:
                        updated_time = row['update_time']
    except Exception as error:
        logging.error('getmtime error: %s', error)
    mtime = time.mktime(time.strptime(updated_time.replace('T', ' '), '%Y-%m-%d %H:%M:%S'))
    return web.Response(text=f'{int(mtime):d}')

@routes.get('/{filename}/last_modified')
async def file_last_modified(request):
    """file last modified"""
    filename = request.match_info.get('filename','')
    updated_time = 0
    if len(filename) > 0 and os.path.isfile(f"./{filename}"):
        updated_time = os.path.getmtime(filename)
    return web.Response(text=f'{int(updated_time):d}')


def main():
    """run httpserver"""
    os.chdir('wwwroot')
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    app.router.add_routes(routes)
    app.router.add_static(prefix='/', path='.', show_index=False)
    web.run_app(app, host='0.0.0.0', port=int(sys.argv[1]))


if __name__ == '__main__':
    main()
