from dice import DICE


def test_both_languages_present():
    assert "de" in DICE
    assert "en" in DICE


def test_all_keys_present():
    for lang in ("de", "en"):
        for key in ("articles", "d1", "d2", "d3", "d4", "d5"):
            assert key in DICE[lang], f"Missing key '{key}' in DICE['{lang}']"


def test_dice_lengths():
    for lang in ("de", "en"):
        for key in ("d1", "d2", "d3", "d4", "d5"):
            assert len(DICE[lang][key]) == 20, (
                f"DICE['{lang}']['{key}'] has {len(DICE[lang][key])} entries, expected 20"
            )


def test_de_articles():
    assert set(DICE["de"]["articles"]) == {"Der", "Die", "Das"}


def test_en_articles():
    assert DICE["en"]["articles"] == ["The"]


def test_no_empty_entries():
    for lang in ("de", "en"):
        for key in ("d1", "d2", "d3", "d4", "d5"):
            for i, entry in enumerate(DICE[lang][key]):
                assert entry.strip() != "", (
                    f"Empty entry at DICE['{lang}']['{key}'][{i}]"
                )


def test_no_duplicate_entries_per_die():
    for lang in ("de", "en"):
        for key in ("d1", "d2", "d3", "d4", "d5"):
            entries = DICE[lang][key]
            assert len(entries) == len(set(entries)), (
                f"Duplicate entries in DICE['{lang}']['{key}']"
            )
