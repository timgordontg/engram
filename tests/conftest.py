import pytest

import engrim.cli as cli


@pytest.fixture(autouse=True)
def _deterministic_embedder(monkeypatch):
    """Keep the suite offline + deterministic. Semantic recall is now ON by default (model2vec is a
    core dependency), so without this every `add`/`assist` could trigger a real model download. We
    force pure-lexical here; semantic tests opt in explicitly by setting cli._EMBEDDER_OVERRIDE."""
    monkeypatch.setenv("ENGRIM_EMBED", "off")
    monkeypatch.setattr(cli, "_EMBEDDER", None, raising=False)
    monkeypatch.setattr(cli, "_EMBEDDER_OVERRIDE", None, raising=False)
    yield
