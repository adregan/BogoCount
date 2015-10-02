import random
import time
import redis
from collections import defaultdict
import logging

r = redis.StrictRedis(host='localhost', port=6379, db=1)
pipe = r.pipeline()

start_time = time.time()
current_count = 0
attempts = 0
count_to = 10
succefully_counted_to = defaultdict(int)

try:
    while True:
        next_number = random.randint(current_count + 1, count_to)

        if current_count + 1 == next_number:
            current_count = next_number
            succefully_counted_to[str(next_number)] += 1
        else:
            if current_count > 6:
                print('failed on attempt {}'.format(attempts))
            attempts += 1
            current_count = 0

        if current_count == count_to:
            total_seconds = time.time() - start_time

            for number, count in succefully_counted_to.items():
                pipe.hincrby('successfullyCountedTo', number, count)

            pipe.rpush(
                'successfulAfterAttempts', attempts
            ).rpush(
                'successfulTimeTaken', total_seconds
            ).set(
                'currentAttempts', 0
            ).incrby(
                'totalAttempts', attempts
            ).execute()

            r.save()

            r.publish('success', True)

            start_time = time.time()
            attempts = 0
            current_count = 0

except KeyboardInterrupt:
    pass
