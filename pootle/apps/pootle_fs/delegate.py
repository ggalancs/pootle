# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from pootle.core.plugin.delegate import Provider


# File system plugins such as git/mercurial/localfs
fs_plugins = Provider()

fs_pre_pull_handlers = Provider()
fs_post_pull_handlers = Provider()
fs_pre_push_handlers = Provider()
fs_post_push_handlers = Provider()
