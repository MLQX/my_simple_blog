# imports
import sqlite3

from flask import Flask, request, session, g, redirect, url_for, abort,  render_template, flash


from contextlib import closing  # 引入closing函数



# configs

DATABASE = './db/blog.db'

DEBUG = True

SECRET_KEY = 'zwb55217421@163.com'

USERNAME = 'ruoan'

PASSWORD = SECRET_KEY[:3]