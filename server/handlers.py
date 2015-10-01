import tornado.web
import tornado.websocket
import tornado.gen as gen
import tornado.escape
from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPRequest

import json
import logging
from functools import reduce


class MainHandler(tornado.web.RequestHandler):

    @property
    def redis(self):
        return self.application.r

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Content-Type', 'application/json')

    def get(self):
        try:
            total_attempts = int(self.redis.get('totalAttempts'))
        except TypeError:
            # Total attempts doesn't exist
            self.write({})
            return

        attemps_until_success, avg_attempts_until_success = (
            self._fetch_lists_and_compute_avg('successfulAfterAttempts'))

        time_until_success, avg_time_until_success = (
            self._fetch_lists_and_compute_avg('successfulTimeTaken'))

        times_successfully_counted_to = (
            self._convert_hash_to_dict('successfullyCountedTo'))

        self.write('hi')

    def _convert_hash_to_dict(self, redis_field):
        data = self.redis.hgetall(redis_field)

        return {
            '{}'.format(key.decode('utf-8')): int(value)
            for key, value in data.items()
        }

    def _fetch_lists_and_compute_avg(self, redis_field):
        def convert_to_int(value):
            try:
                return int(value)
            except ValueError:
                return int(float(value))

        length_of_data = self.redis.llen(redis_field)
        data = self.redis.lrange(redis_field, 0, (length_of_data - 1))

        list_of_data = [
            convert_to_int(value) for value in data
        ]

        avg_of_list = int(reduce(
            lambda x, y: x + y, list_of_data) / length_of_data
        )

        return list_of_data, avg_of_list

class WebSocket(tornado.websocket.WebSocketHandler):

    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        self.write_message(u"You said: " + message)

    def on_close(self):
        print("WebSocket closed")
