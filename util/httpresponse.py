#!/usr/bin/env python2.7
#
# -*- coding:utf-8 -*-
#
#   Author  :   YunJianFei
#   E-mail  :   yunjianfei@126.com
#   Date    :   2014/02/25
#   Desc    :   Test db
#
#

import json,logging,types
from util import tools

class ResponseCode:
    SUCCESS = 0
    NO_PARAMETER = 1
    INVALID_PARAMETER = 2
    HAS_EXISTED = 3
    DB_ERROR = 4
    NO_RECORD = 5
    DELAY = 6

    code_string_EN = {
        SUCCESS : "SUCCESS",
        NO_PARAMETER : "NO_PARAMETER",
        INVALID_PARAMETER : "INVALID_PARAMETER",
        HAS_EXISTED : "HAS_EXISTED",
        DB_ERROR : "DB_ERROR",
        NO_RECORD : "NO_RECORD",
        DELAY : "DELAY"
    }

    failure_reason_EN = {
        SUCCESS : "%s success!",
        NO_PARAMETER : "There is no parameter '%s'!",
        INVALID_PARAMETER : "The value of parameter '%s' is invalid!",
        HAS_EXISTED : "This object has existed in the table '%s'!",
        DB_ERROR : "Database error when execute '%s'!",
        NO_RECORD : "No record when query '%s'!",
        DELAY : " Delay '%s' days!",
    }

class Response:
    def to_int(self, num):
        if num == None:
            return num

        try:
            num = tools.strip_string(num) 
            value = int(num)
            return value
        except Exception, ex:
            logging.error("Convert '%s' to Int Error: %s", str(num), str(ex))
            return None


    def make_response(self, code, para=None, content=None, err_str=None):
        response = {}
        response['response_code'] = code
        response['response_code_string'] = ResponseCode.code_string_EN[code]

        failure_reason = ""
        if code != ResponseCode.SUCCESS:
            if para != None:
                failure_reason = ResponseCode.failure_reason_EN[code] % para

            if err_str != None:
                failure_reason = failure_reason + err_str

            response['failure_reason'] = failure_reason

        if content != None:
            response['content'] = content
            
        if para != None:
            success_type = ResponseCode.failure_reason_EN[code] % para
            response['success_type'] = success_type
        

        return json.dumps(response, default=tools.json_date_default)
