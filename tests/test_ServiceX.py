# Tests to make sure we get at the functionality in the remote executor.
import ast
import ast
import asyncio

from func_adl import EventDataset
import pandas as pd
import pytest
from servicex import ServiceXDataset

from func_adl_xAOD import ServiceXDatasetSource

async def do_exe(a):
    return a

def get_async_mock(mocker):
    import sys
    if sys.version_info[1] <= 7:
        import asyncmock
        return asyncmock.MagicMock
    else:
        return mocker.MagicMock

@pytest.fixture()
def simple_Servicex_fe_watcher(mocker):
    'Mock out the servicex guy'
    m_servicex = get_async_mock(mocker)(spec=ServiceXDataset)
    m_servicex.get_data_pandas_df_async.return_value = pd.DataFrame()
    p_servicex = mocker.patch('func_adl_xAOD.ServiceX.ServiceXDataset', return_value=m_servicex)
    return m_servicex, p_servicex
    

def test_find_EventDataSet_good():
    a = ServiceXDatasetSource("file://junk.root") \
        .value(executor=do_exe)

    assert isinstance(a, ast.Call)


def test_as_qastle():
    a = ServiceXDatasetSource("file://junk.root")
    from qastle import python_ast_to_text_ast
    q = python_ast_to_text_ast(a._ast)
    assert q.startswith("(call EventDataset 'ServiceXDatasetSource_")


@pytest.mark.asyncio
async def test_pandas_query(simple_Servicex_fe_watcher):
    'Simple pandas based query'
    f_ds = ServiceXDatasetSource(r'bogus_ds')
    r = await f_ds \
        .SelectMany('lambda e: e.Jets("AntiKt4EMTopoJets")') \
        .Select('lambda j: j.pt()/1000.0') \
        .AsPandasDF('JetPt') \
        .value_async()
    assert r is not None
    assert isinstance(r, pd.DataFrame)
    assert len(r) == 0

    caller = simple_Servicex_fe_watcher[0].get_data_pandas_df_async
    caller.assert_called_once()
    args = caller.call_args[0]
    kwargs = caller.call_args[1]
    assert len(args) == 1
    assert args[0].find('SelectMany') >= 0
    assert args[0].startswith('(call ResultTTree')


@pytest.mark.asyncio
async def test_awkward_query(simple_Servicex_fe_watcher):
    'Simple pandas based query'
    f_ds = ServiceXDatasetSource(r'bogus_ds')
    await f_ds \
        .SelectMany('lambda e: e.Jets("AntiKt4EMTopoJets")') \
        .Select('lambda j: j.pt()/1000.0') \
        .AsAwkwardArray('JetPt') \
        .value_async()

    caller = simple_Servicex_fe_watcher[0].get_data_awkward_async
    caller.assert_called_once()
    args = caller.call_args[0]
    assert len(args) == 1
    assert args[0].find('SelectMany') >= 0
    assert args[0].startswith('(call ResultTTree')


@pytest.mark.asyncio
async def test_scoped_dataset_name(simple_Servicex_fe_watcher):
    'Simple pandas based query'
    f_ds = ServiceXDatasetSource(r'user.fork:bogus_ds')
    r = await f_ds \
        .SelectMany('lambda e: e.Jets("AntiKt4EMTopoJets")') \
        .Select('lambda j: j.pt()/1000.0') \
        .AsPandasDF('JetPt') \
        .value_async()

    simple_Servicex_fe_watcher[1].assert_called_once()
    assert simple_Servicex_fe_watcher[1].call_args[0][0] == 'user.fork:bogus_ds'
