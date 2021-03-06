# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

import logging

from translate.storage.factory import getclass

from django.utils.translation import ugettext as _

from pootle_app.models.permissions import check_user_permission
from pootle_statistics.models import SubmissionTypes
from pootle_store.models import Store

from .exceptions import (FileImportError, MissingPootlePathError,
                         MissingPootleRevError, UnsupportedFiletypeError)


logger = logging.getLogger(__name__)


def import_file(file, user=None):
    f = getclass(file)(file.read())
    if not hasattr(f, "parseheader"):
        raise UnsupportedFiletypeError(_("Unsupported filetype '%s', only PO "
                                         "files are supported at this time\n",
                                         file.name))
    header = f.parseheader()
    pootle_path = header.get("X-Pootle-Path")
    if not pootle_path:
        raise MissingPootlePathError(_("File '%s' missing X-Pootle-Path "
                                       "header\n", file.name))

    rev = header.get("X-Pootle-Revision")
    if not rev or not rev.isdigit():
        raise MissingPootleRevError(_("File '%s' missing or invalid "
                                      "X-Pootle-Revision header\n",
                                      file.name))
    rev = int(rev)

    try:
        store, created = Store.objects.get_or_create(pootle_path=pootle_path)
    except Exception as e:
        raise FileImportError(_("Could not create '%s'. Missing "
                                "Project/Language? (%s)", (file.name, e)))

    tp = store.translation_project
    allow_add_and_obsolete = ((tp.project.checkstyle == 'terminology'
                               or tp.is_template_project)
                              and check_user_permission(user,
                                                        'administrate',
                                                        tp.directory))
    try:
        store.update(store=f, user=user,
                     submission_type=SubmissionTypes.UPLOAD,
                     store_revision=rev,
                     allow_add_and_obsolete=allow_add_and_obsolete)
    except Exception as e:
        # This should not happen!
        logger.error("Error importing file: %s", str(e))
        raise FileImportError(_("There was an error uploading your file"))
