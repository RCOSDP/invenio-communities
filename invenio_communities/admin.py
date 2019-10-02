# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015, 2016 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Admin model views for Communities."""

from __future__ import absolute_import, print_function
from flask import current_app
from flask_admin.contrib.sqla import ModelView

from .models import Community, FeaturedCommunity, InclusionRequest
from wtforms.validators import ValidationError
import re

def _(x):
    """Identity function for string extraction."""
    return x


class CommunityModelView(ModelView):
    """ModelView for the Community."""

    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    column_display_all_relations = True
    form_columns = ('id', 'owner', 'index', 'title', 'description', 'page',
                    'curation_policy', 'ranking', 'fixed_points')
    column_list = (
        'id',
        'title',
        'owner.id',
        'index.index_name',
        'deleted_at',
        'last_record_accepted',
        'ranking',
        'fixed_points',
    )
    column_searchable_list = ('id', 'title', 'description')


    def _validate_input_id(form, field):
        the_patterns = {
            "ASCII_LETTER_PATTERN": "[\x20-\x7F]",
            "FIRST_LETTER_PATTERN": "^[a-zA-Z].*",
            "PUNCTUATION_PATTERN": "[\x20-\x2C]|[\x2E-\x2F]|[\x3A-\x40]|[\x5D-\x5E]|[\x7B-\x7E]|[\x5B]|[\x60]",

        }

        the_result = {
            "ASCII_LETTER_PATTERN": "The character must be ASCII.",
            "FIRST_LETTER_PATTERN": "The first character must be alphabet.",
            "PUNCTUATION_PATTERN": "Puntuation character require escape backslash"
        }

        for pattern in the_patterns:
            try:
                if pattern == 'PUNCTUATION_PATTERN':
                    count_puntuation = len(re.findall(the_patterns[pattern],
                                                      field.data))
                    backslask_pattern = \
                        r"\\[\x20-\x2C]|[\x2E-\x2F]|[\x3A-\x40]|[\x5D-\x5E]|[\x7B-\x7E]|[\x5B]|[\x60]"
                    count_backslask = len(re.findall(backslask_pattern, field.data))
                    if count_puntuation != count_backslask:
                        ValidationError(the_result[pattern])
                        break
                else:
                    m = re.match(the_patterns[pattern], field.data)
                    if (m is None):
                        raise ValidationError(the_result[pattern])
                        break
            except Exception as ex:
                raise ValidationError('{}'.format(ex))

    form_args = {
        'id': {
            'validators': [_validate_input_id]
        }
    }

    form_edit_rules = (
        'id')

    form_widget_args = {
        'id': {
            'disabled': True
        }
    }


class FeaturedCommunityModelView(ModelView):
    """ModelView for the FeaturedCommunity."""

    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_display_all_relations = True
    column_list = (
        'community',
        'start_date',
    )


class InclusionRequestModelView(ModelView):
    """ModelView of the InclusionRequest."""

    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True
    column_list = (
        'id_community',
        'id_record',
        'expires_at',
        'id_user'
    )


community_adminview = dict(
    model=Community,
    modelview=CommunityModelView,
    category=_('Communities'),
)

request_adminview = dict(
    model=InclusionRequest,
    modelview=InclusionRequestModelView,
    category=_('Communities'),
)

featured_adminview = dict(
    model=FeaturedCommunity,
    modelview=FeaturedCommunityModelView,
    category=_('Communities'),
)
