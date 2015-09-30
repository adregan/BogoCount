import random
import time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)
pipe = r.pipeline()

start_time = time.time()
current_count = 0
attempts = 0
count_to = 10

while True:
    next_number = random.randint(1, count_to)

    if current_count + 1 == next_number:
        current_count = next_number
        pipe.incr(str(next_number))
    else:
        attempts += 1
        if current_count > 6:
            print('failed on attempt #{}'.format(attempts))
        # r.incr('currentAttempts')
        current_count = 0

    if current_count == count_to:
        total_seconds = time.time() - start_time
        pipe.rpush(
            'successfulAfterAttempts', attempts
        ).rpush(
            'successfulTimeTaken', total_seconds
        ).set(
            'currentAttempts', 0
        ).incrby(
            'totalAttempts', attempts
        ).execute()

        print('Successfully counted to {} after {} attempts'.format(count_to, attempts))

        start_time = time.time()
        attempts = 0
