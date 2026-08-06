#!/usr/bin/env python3
"""
Multi-editor pool for XNOQuant submission.

Loads editor IDs from .env (XNO_EDITOR_MID_01 .. XNO_EDITOR_MID_10) and
provides round-robin rotation for distributing alpha submissions across
multiple XNOQuant editors.

Usage:
    from editor_pool import EditorPool

    pool = EditorPool(prefix="XNO_EDITOR_MID")
    for filepath in files:
        editor_id, base_url = pool.get_next()
        # submit using this editor
"""

import os


class EditorPool:
    """Round-robin pool of XNOQuant editor IDs.

    Loads up to 10 editor UUIDs from environment variables named
    {prefix}_01 through {prefix}_10. Each editor maps to a base URL
    for the XNOQuant /editors/{id} API.
    """

    API_BASE = "https://api.xnoquant.io/xalpha-api/v2/editors"

    def __init__(self, prefix="XNO_EDITOR_MID", token=None):
        """Load editors from env and set up round-robin.

        Args:
            prefix: Environment variable prefix (default: XNO_EDITOR_MID).
                    Looks for {prefix}_01 .. {prefix}_10.
            token: XNO token. If None, reads from os.getenv("XNO_TOKEN").
        """
        self.editors = []  # list of (editor_id, base_url)
        self._index = 0
        self._usage_count = {}  # editor_id -> count of submissions

        for i in range(1, 11):
            env_key = f"{prefix}_{i:02d}"
            editor_id = os.getenv(env_key, "").strip()
            if editor_id:
                base = f"{self.API_BASE}/{editor_id}"
                self.editors.append((editor_id, base))
                self._usage_count[editor_id] = 0

        self.token = token or os.getenv("XNO_TOKEN", "").strip()

    def get_next(self):
        """Return (editor_id, base_url) for the next submission (round-robin).

        Returns:
            Tuple of (editor_id, base_url).

        Raises:
            RuntimeError: If no editors are loaded.
        """
        if not self.editors:
            raise RuntimeError(
                "No editors loaded. Add XNO_EDITOR_MID_01 .. XNO_EDITOR_MID_10 to .env"
            )
        editor_id, base_url = self.editors[self._index % len(self.editors)]
        self._index += 1
        self._usage_count[editor_id] = self._usage_count.get(editor_id, 0) + 1
        return editor_id, base_url

    def get_all(self):
        """Return list of all (editor_id, base_url) tuples."""
        return list(self.editors)

    def count(self):
        """Return number of editors in pool."""
        return len(self.editors)

    def usage_summary(self):
        """Return dict of {editor_id: submission_count}."""
        return dict(self._usage_count)

    def is_configured(self):
        """Return True if at least one editor and a token are loaded."""
        return bool(self.editors and self.token)

    def __repr__(self):
        return f"EditorPool(editors={self.count()}, token={'***' if self.token else 'MISSING'})"
