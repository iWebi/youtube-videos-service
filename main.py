#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json

import webapp2

from service import get_latest_videos_from_channel_ids
from util import get_json_from_request_body


class YoutubeSearchHandler(webapp2.RequestHandler):
    def post(self):
        search_options = get_json_from_request_body(self.request)
        videos = get_latest_videos_from_channel_ids(search_options)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(videos))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


app = webapp2.WSGIApplication(
    [('/', MainHandler), ('/youtube/channel_videos', YoutubeSearchHandler)],
    debug=True)