"""
Test the main KojiWrapper class
"""

import pytest
import koji
from koji_wrapper.wrapper import KojiWrapper
from unittest.mock import MagicMock

sample_url = 'http://kojihub.com'
sample_topurl = 'http://somerepo.org'

@pytest.fixture()
def a_koji_wrapper():
    return build_wrapper(None)

def build_wrapper(this_session):
    return KojiWrapper( url = sample_url,
                        topurl = sample_topurl,
                        session = this_session)

def test_set_init_values():
    """
    GIVEN KojiWrapper initialized with no session
    WHEN the object is created
    THEN session is set to an instance of koji.ClientSession
    AND we should have properly set url and topurl
    """
    test_wrapper = build_wrapper(None)
    assert test_wrapper.url == sample_url
    assert test_wrapper.topurl == sample_topurl
    assert isinstance(test_wrapper.session,koji.ClientSession)

def test_init_with_koji_client_session():
    """
    GIVEN we have a valid koji.ClientSession object,
    WHEN this object is passed as the session to a new KojiWrapper
    THEN this object's session is set to the session of the passed object
    """
    client_session = MagicMock(spec=koji.ClientSession)
    test_wrapper = build_wrapper(client_session)
    assert isinstance(test_wrapper.session,koji.ClientSession)

def test_init_with_koji_wrapper():
    """
    GIVEN we have a valid KojiWrapper with a session,
    WHEN a KojiWrapper object is passed as the session to a new KojiWrapper
    THEN this object's session is set to the session of the passed object
    """
    my_koji_wrapper = build_wrapper(None)
    test_wrapper = build_wrapper(my_koji_wrapper)
    assert isinstance(test_wrapper.session,koji.ClientSession)
    assert test_wrapper.session is my_koji_wrapper.session

def test_gets_build(a_koji_wrapper, sample_build):
    """
    GIVEN we have a valid KojiWrapper with a session,
    WHEN we call the build method with a valid nvr,
    THEN we get a build object back from the koji api
    """
    a_koji_wrapper.session.getBuild = MagicMock(return_value=sample_build)
    b = a_koji_wrapper.build('some_nvr')
    assert a_koji_wrapper.session.getBuild.called
    assert isinstance(b,dict)
    assert 'id' in b

def test_gets_archives(a_koji_wrapper, sample_archives):
    """
    GIVEN we have a valid KojiWrapper with a session,
    WHEN we call the archives method with a valid build id and type,
    THEN we get a list of achives back from the koji api
    """
    a_koji_wrapper.session.listArchives = MagicMock(return_value=sample_archives)
    arc = a_koji_wrapper.archives(buildID='12345', type='image')
    assert a_koji_wrapper.session.listArchives.called
    assert isinstance(arc,list)

def test_returns_file_types(a_koji_wrapper, sample_archives):
    """
    GIVEN we have a valid KojiWrapper with a session,
    WHEN we call the archives method with a valid build id and type,
    THEN we get a list of file_types in the archive for the given nvr
    """
    a_koji_wrapper.session.listArchives = \
        MagicMock(return_value=sample_archives)
    a_koji_wrapper.session.getBuild = MagicMock(return_value={'id':'12345'})
    ft = a_koji_wrapper.file_types('myproject-9.0-20190326.1.el7ost')
    assert a_koji_wrapper.session.getBuild.called
    assert a_koji_wrapper.session.listArchives.called
    assert isinstance(ft,list)
    assert 'image' in ft

