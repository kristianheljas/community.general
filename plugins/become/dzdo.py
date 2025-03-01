# -*- coding: utf-8 -*-
# Copyright (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import annotations

DOCUMENTATION = r"""
name: dzdo
short_description: Centrify's Direct Authorize
description:
  - This become plugins allows your remote/login user to execute commands as another user using the C(dzdo) utility.
author: Ansible Core Team
options:
  become_user:
    description: User you 'become' to execute the task.
    type: string
    ini:
      - section: privilege_escalation
        key: become_user
      - section: dzdo_become_plugin
        key: user
    vars:
      - name: ansible_become_user
      - name: ansible_dzdo_user
    env:
      - name: ANSIBLE_BECOME_USER
      - name: ANSIBLE_DZDO_USER
  become_exe:
    description: C(dzdo) executable.
    type: string
    default: dzdo
    ini:
      - section: privilege_escalation
        key: become_exe
      - section: dzdo_become_plugin
        key: executable
    vars:
      - name: ansible_become_exe
      - name: ansible_dzdo_exe
    env:
      - name: ANSIBLE_BECOME_EXE
      - name: ANSIBLE_DZDO_EXE
  become_flags:
    description: Options to pass to C(dzdo).
    type: string
    default: -H -S -n
    ini:
      - section: privilege_escalation
        key: become_flags
      - section: dzdo_become_plugin
        key: flags
    vars:
      - name: ansible_become_flags
      - name: ansible_dzdo_flags
    env:
      - name: ANSIBLE_BECOME_FLAGS
      - name: ANSIBLE_DZDO_FLAGS
  become_pass:
    description: Options to pass to C(dzdo).
    type: string
    required: false
    vars:
      - name: ansible_become_password
      - name: ansible_become_pass
      - name: ansible_dzdo_pass
    env:
      - name: ANSIBLE_BECOME_PASS
      - name: ANSIBLE_DZDO_PASS
    ini:
      - section: dzdo_become_plugin
        key: password
"""

from ansible.plugins.become import BecomeBase


class BecomeModule(BecomeBase):

    name = 'community.general.dzdo'

    # messages for detecting prompted password issues
    fail = ('Sorry, try again.',)

    def build_become_command(self, cmd, shell):
        super(BecomeModule, self).build_become_command(cmd, shell)

        if not cmd:
            return cmd

        becomecmd = self.get_option('become_exe')

        flags = self.get_option('become_flags')
        if self.get_option('become_pass'):
            self.prompt = f'[dzdo via ansible, key={self._id}] password:'
            flags = f"{flags.replace('-n', '')} -p \"{self.prompt}\""

        become_user = self.get_option('become_user')
        user = f'-u {become_user}' if become_user else ''

        return f"{becomecmd} {flags} {user} {self._build_success_command(cmd, shell)}"
