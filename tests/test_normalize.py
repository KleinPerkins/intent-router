"""L0 normalize tests — pure, deterministic tokenization (ARCHITECTURE.md L0)."""

from __future__ import annotations

import unittest

from intent_router.normalize import build_alias_to_canon, normalize_text, normalize_tokens, singularize


class TestNormalizeTokens(unittest.TestCase):
    def test_empty_text_is_empty_set(self):
        self.assertEqual(normalize_tokens(""), frozenset())
        self.assertEqual(normalize_tokens(None), frozenset())  # type: ignore[arg-type]

    def test_lowercases_and_splits(self):
        toks = normalize_tokens("Put THIS Work Somewhere Safe")
        self.assertEqual(toks, normalize_tokens("put this work somewhere safe"))
        self.assertIn("work", toks)
        self.assertIn("safe", toks)

    def test_question_mark_does_not_change_tokens(self):
        self.assertEqual(normalize_tokens("is everything okay?"), normalize_tokens("is everything okay"))

    def test_stopwords_removed_pre_and_post_singularize(self):
        # Regression: "this" must not survive as a naive-singularized "thi".
        toks = normalize_tokens("this is my repo")
        self.assertNotIn("thi", toks)
        self.assertNotIn("this", toks)
        self.assertIn("repo", toks)

    def test_deterministic_repeat_calls(self):
        a = normalize_tokens("clean up my old safe copy")
        b = normalize_tokens("clean up my old safe copy")
        self.assertEqual(a, b)
        self.assertIsInstance(a, frozenset)

    def test_is_a_pure_function_no_shared_mutable_state(self):
        acronyms = {"repo": "repository"}
        first = normalize_tokens("repo status", acronyms=acronyms)
        # Mutating the caller's dict after the call must not affect a fresh call's behavior for the
        # SAME logical inputs (no hidden module-level caching keyed incorrectly).
        acronyms["repo"] = "something else entirely"
        second_same_input = normalize_tokens("repo status", acronyms={"repo": "repository"})
        self.assertEqual(first, second_same_input)

    def test_singularize_conservative_on_short_or_double_s(self):
        self.assertEqual(singularize("gas"), "gas")  # len <= 3 -> unchanged
        self.assertEqual(singularize("class"), "class")  # ends with 'ss' -> unchanged
        self.assertEqual(singularize("copies"), "copy")
        self.assertEqual(singularize("boxes"), "box")
        self.assertEqual(singularize("copy"), "copy")

    def test_acronym_expansion_is_additive(self):
        toks = normalize_tokens("pr status", acronyms={"pr": "pull request"})
        self.assertIn("pr", toks)  # additive: original token kept
        self.assertIn("pull", toks)
        self.assertIn("request", toks)

    def test_synonym_expansion_bidirectional(self):
        synonyms = {"safe": ["protected", "secure"]}
        alias_to_canon = build_alias_to_canon(synonyms)
        self.assertEqual(alias_to_canon["protected"], "safe")
        toks_canon = normalize_tokens("keep this safe", synonyms=synonyms)
        toks_alias = normalize_tokens("keep this protected", synonyms=synonyms)
        # Canonical form appears when the alias is used, so overlap scoring can match either way.
        self.assertIn("safe", toks_canon)
        self.assertIn("safe", toks_alias)


class TestNormalizeText(unittest.TestCase):
    def test_collapses_whitespace_and_lowers(self):
        self.assertEqual(normalize_text("  Is   Everything   OK?  "), "is everything ok?")

    def test_empty(self):
        self.assertEqual(normalize_text(""), "")
        self.assertEqual(normalize_text(None), "")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
