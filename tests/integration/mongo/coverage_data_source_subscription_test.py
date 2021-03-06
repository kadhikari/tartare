# coding=utf-8

# Copyright (c) 2001-2016, Canal TP and/or its affiliates. All rights reserved.
#
# This file is part of Navitia,
#     the software to build cool stuff with public transport.
#
# Hope you'll enjoy and contribute to this project,
#     powered by Canal TP (www.canaltp.fr).
# Help us simplify mobility and open public transport:
#     a non ending quest to the responsive locomotion way of traveling!
#
# LICENCE: This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# Stay tuned using
# twitter @navitia
# IRC #navitia on freenode
# https://groups.google.com/d/forum/navitia
# www.navitia.io
from tests.utils import to_json, post, delete
import json


def test_bad_coverage(app):
    raw = post(app, '/coverages/unknown/data_sources',
               '''{"id": "bob"}''')
    r = to_json(raw)
    assert raw.status_code == 404
    assert r.get('error') == 'Coverage unknown not found.'


def test_missing_data_source_id(app, coverage):
    raw = post(app, '/coverages/jdr/data_sources',
               '''{}''')
    r = to_json(raw)
    assert raw.status_code == 400
    assert r.get('error') == 'Missing data_source_id attribute in request body.'


def test_unknown_data_source(app, coverage):
    raw = post(app, '/coverages/jdr/data_sources',
               '''{"id": "bob"}''')
    r = to_json(raw)
    assert raw.status_code == 404
    assert r.get('error') == 'Data source bob not found.'


def test_add_data_source(app, coverage, data_source):
    raw = post(app, '/coverages/jdr/data_sources',
               json.dumps({"id": data_source.get('id')}))
    r = to_json(raw)
    assert raw.status_code == 200
    data_sources = r.get('coverages')[0].get('data_sources')
    assert isinstance(data_sources, list)
    assert len(data_sources) == 1
    assert data_sources[0] == data_source.get('id')

    # test add existing data_source in coverage
    raw = post(app, '/coverages/jdr/data_sources',
               json.dumps({"id": data_source.get('id')}))
    r = to_json(raw)
    assert raw.status_code == 409
    assert r.get('error') == 'Data source id {} already exists in coverage jdr.'.format(data_source.get('id'))


def test_delete_unknown_coverage(app):
    raw = delete(app, '/coverages/jdr/data_sources/toto')
    r = to_json(raw)
    assert raw.status_code == 404
    assert r.get('error') == 'Unknown coverage id "jdr".'

def test_delete_unknown_data_source(app, coverage_with_data_source_tram_lyon):
    raw = delete(app, '/coverages/jdr/data_sources/toto')
    r = to_json(raw)
    assert raw.status_code == 404
    assert r.get('error') == 'Unknown data source id "toto" attribute in uri.'


def test_delete_valid_data_source(app, coverage_with_data_source_tram_lyon):
    assert 'tram_lyon' in coverage_with_data_source_tram_lyon['data_sources']
    raw = delete(app, '/coverages/jdr/data_sources/tram_lyon')
    assert raw.status_code == 204
    jdr_cov = to_json(app.get('/coverages/jdr'))
    assert 'data_sources' not in jdr_cov
