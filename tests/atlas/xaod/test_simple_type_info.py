import func_adl_xAOD.common.cpp_types as ctyp
from func_adl_xAOD.common.ast_to_cpp_translator import xAODTranslationError
from tests.atlas.xaod.utils import atlas_xaod_dataset  # type: ignore

# Test the simple type information system.


def test_cant_call_double():
    msg = ""
    try:
        atlas_xaod_dataset("file://root.root") \
            .Select("lambda e: e.Jets('AntiKt4EMTopoJets').Select(lambda j: j.pt().eta()).Sum()") \
            .value()
    except xAODTranslationError as e:
        msg = str(e)

    assert 'Unable to call method eta on type double' in msg


def test_can_call_prodVtx():
    ctyp.add_method_type_info("xAOD::TruthParticle", "prodVtx", ctyp.terminal('xAODTruth::TruthVertex', is_pointer=True))
    atlas_xaod_dataset("file://root.root") \
        .Select("lambda e: e.TruthParticles('TruthParticles').Select(lambda t: t.prodVtx().x()).Sum()") \
        .value()
