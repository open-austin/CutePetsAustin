#!/usr/bin/env python
# -*- coding: utf-8 -*-

import meow


def lambda_handler(event, context):
    meow.main()


if __name__ == '__main__':
    lambda_handler(None, None)
