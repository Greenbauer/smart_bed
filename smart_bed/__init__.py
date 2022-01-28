'''
Start of app


bed:
    fun mode off:
        no users:
            (ambient lights turn on after sunset)
            when a user enters the bed:
                (ambient lights turn off)
                (broadcast state)
        one user:
            when they stay in bed:
                (ambient lights stay off)
            when they leave the bed:
                (broadcast state)
                when they are finished sleeping:
                    (ambient lights turn on after sunrise for a few minutes)
                when they are going back to bed:
                    (ambient night light turns on from the side they got out of for a few minutes)
            when another user enters the bed:
                (broadcast state)
                (ambient lights stay off)
        two users:
            when one user leaves the bed:
                (broadcast state)
                when they are finished sleeping:
                    (ambient lights stay off)
                when they are going back to bed:
                    (ambient night light turns on from the side they got out of for a few minutes)
            when both users stay in bed:
                (ambient lights stay off)
            when both users leave the bed:
                (broadcast state)
                when they are finished sleeping:
                    (ambient lights turn on after sunrise for a few minuets)
                when they are going back to bed:
                    (ambient night light turns on from the side they got out of for a few minutes)
     fun mode on:
        (ambient fun mode lights turn on)
        (broadcast state)
'''

__author__ = '''Zachary Greenbauer'''
__version__ = '1.0.0'


import environment
import smart_bed.tasks
import smart_bed.listener
import smart_bed.api
