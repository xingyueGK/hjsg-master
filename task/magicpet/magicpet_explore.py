#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/30 21:28
# @Author  : xingyue
# @File    : magicpet_explore.py


class MagicpetExplore(object):

    def index(self):

        index = self.action(c='magicpet_explore',m='index')
        self.logger.info('Get MagicpetExplore Index %s'%index )
        return index

    def area_reward_into(self,area_id=1):
        area_reward_into =self.action(c='magicpet_explore',m='area_reward_into',area_id=area_id)
        self.logger.info('Get area_reward_into Index %s' % area_reward_into)
        return area_reward_into

    def one_button_join(self):
        self.action(c='magicpet_explore',m='one_button_join')

    def explore_start(self,area_id=1):
        self.logger.info('explore_start')
        status = self.action(c='magicpet_explore',m='explore_start',area_id=area_id,tenfold_addition_price='undefined')

        self.logger.info('explore_start %s'%status)

