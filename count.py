import random
import time
import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

start_time = time.time()
finished_counting = False
current_count = 0
attempts = 0
count_to = 10

while True:
    if current_count == count_to:
        # Record the success 
        total_seconds = time.time() - start_time

    next_number = random.randint(1, count_to)

    if current_count + 1 == next_number:
        current_count = next_number
        # Here iterate the stored data
    else:
        attempts += 1
        current_count = 0
        # Record another attempt
