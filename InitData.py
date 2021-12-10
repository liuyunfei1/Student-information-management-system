import redis
import json

db2 = redis.Redis(host='127.0.0.1', port=6379, db=3, decode_responses=True)
db1 = redis.Redis(host='127.0.0.1', port=6379, db=2, decode_responses=True)
db0 = redis.Redis(host='127.0.0.1', port=6379, db=1, decode_responses=True)
db2.hset('student', '201512101111', json.dumps(
    {'schoolnumber': '201512101111', 'name': '杨小颖', 'chinese': 89,
     'math': 84, 'english': 85, 'total': 258}))
db0.hset('student', '201512101111', json.dumps(
    {'schoolnumber': '201512101111', 'name': '杨小颖', 'chinese': 79,
     'math': 74, 'english': 75, 'total': 228}))
db1.set('201512101111', '123456')
db2.hset('student', '201623202222', json.dumps(
    {'schoolnumber': '201623202222', 'name': '刘小菲', 'chinese': 75,
     'math': 70, 'english': 96, 'total': 241}))
db0.hset('student', '201623202222', json.dumps(
    {'schoolnumber': '201623202222', 'name': '刘小菲', 'chinese': 65,
     'math': 60, 'english': 86, 'total': 211}))
db1.set('201623202222', '123456')
db2.hset('student', '201734303333', json.dumps(
    {'schoolnumber': '201734303333', 'name': '关小彤', 'chinese': 100,
     'math': 100, 'english': 100, 'total': 300}))
db0.hset('student', '201734303333', json.dumps(
    {'schoolnumber': '201734303333', 'name': '关小彤', 'chinese': 90,
     'math': 90, 'english': 90, 'total': 270}))
db1.set('201734303333', '123456')
db2.hset('student', '201845404444', json.dumps(
    {'schoolnumber': '201845404444', 'name': '华小宇', 'chinese': 60,
     'math': 60, 'english': 60, 'total': 180}))
db0.hset('student', '201845404444', json.dumps(
    {'schoolnumber': '201845404444', 'name': '华小宇', 'chinese': 50,
     'math': 50, 'english': 50, 'total': 150}))
db1.set('201845404444', '123456')