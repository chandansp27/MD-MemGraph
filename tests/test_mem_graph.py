"""
Regression tests for mem_graph.py

Run with: python3 tests/test_mem_graph.py
"""

import subprocess
import sys
import tempfile
import os
from pathlib import Path


MEM_GRAPH = ["python3", "src/mem_graph.py"]
ROOT = ["--root", "docs"]


def run(args: list) -> tuple[int, str, str]:
    result = subprocess.run(
        MEM_GRAPH + ROOT + args,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def run_in_subprocess(cmd: list) -> tuple[int, str, str]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def test_heading_level_2_is_node():
    """Test that ## headings define graph nodes."""
    code, stdout, stderr = run(["headers", "--file", "attention.md", "--all"])
    assert code == 0, f"headers failed: {stderr}"
    assert "Attention Limits" in stdout
    assert "attention.md#attention-limits" in stdout
    print("PASS: level-2 heading is a node")


def test_level_1_heading_not_node():
    """Test that # headings are ignored for graph nodes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs = Path(tmpdir) / "docs"
        docs.mkdir()
        (docs / "test.md").write_text("""# Title With Hash

Content here.

---

## Actual Node

This should be a node.
""")
        code, stdout, stderr = run_in_subprocess(
            ["python3", "src/mem_graph.py", "--root", str(docs), "headers", "--file", "test.md", "--all"]
        )
        assert code == 0, f"headers failed: {stderr}"
        assert "Title With Hash" not in stdout
        assert "test.md#title-with-hash" not in stdout
        assert "Actual Node" in stdout
        assert "test.md#actual-node" in stdout
    print("PASS: level-1 heading is not a node")


def test_check_passes_after_heading_fix():
    """Test that check passes with properly formatted docs."""
    code, stdout, stderr = run(["check"])
    assert code == 0, f"Expected OK but got: {stderr}"
    assert "OK" in stdout
    print("PASS: check passes with fixed docs")


def test_inline_code_links_ignored():
    """Test that links inside inline code spans are ignored."""
    code, stdout, stderr = run(["view", "--file", "format.md", "--header", "Link Resolution Rules"])
    assert code == 0, f"view failed: {stderr}"
    assert "links.md#links" in stdout
    print("PASS: inline code links are ignored")


def test_graph_file_and_header_disambiguation():
    """Test that graph respects --file with --header."""
    code, stdout, stderr = run(["graph", "--file", "overview.md", "--header", "Core Philosophy"])
    assert code == 0, f"Expected success but got: {stderr}"
    assert "Core Philosophy" in stdout
    assert "overview.md#core-philosophy" in stdout
    assert "attention.md" not in stdout
    print("PASS: graph --file --header disambiguates")


def test_graph_ambiguous_shows_error():
    """Test that ambiguous header shows helpful error."""
    code, stdout, stderr = run(["graph", "--header", "Overview"])
    assert code == 1
    assert "multiple blocks matched" in stderr
    print("PASS: ambiguous header shows helpful error")


def test_nonexistent_shows_similar_suggestions():
    """Test that nonexistent header suggests similar ones."""
    code, stdout, stderr = run(["graph", "--header", "Nonexistent"])
    assert code == 1
    assert "no matching block found" in stderr
    assert "similar headers" in stderr
    print("PASS: nonexistent header suggests similar")


def test_errors_go_to_stderr():
    """Test that errors are printed to stderr."""
    code, stdout, stderr = run(["graph", "--header", "Nonexistent"])
    assert code == 1
    assert "no matching block found" in stderr
    assert "no matching block found" not in stdout
    print("PASS: errors go to stderr")


def test_check_output_has_line_numbers():
    """Test that check output includes file:line format."""
    code, stdout, stderr = run(["check"])
    if "unresolved" in stderr or "duplicate" in stderr:
        lines = stderr.strip().split("\n")
        for line in lines:
            if "unresolved" in line or "duplicate" in line:
                parts = line.split(":")
                assert len(parts) >= 3, f"Expected file:line format but got: {line}"
    print("PASS: check output has file:line format")


def test_view_nonexistent_shows_helpful_message():
    """Test that view shows helpful message for nonexistent block."""
    code, stdout, stderr = run(["view", "--header", "Fake Header That Does Not Exist"])
    assert code == 1
    assert "no matching block found" in stderr
    print("PASS: view shows helpful message for nonexistent")


def test_view_shows_connections():
    """Test that view shows block connections."""
    code, stdout, stderr = run(["view", "--file", "attention.md", "--header", "Attention Limits"])
    assert code == 0
    assert "->" in stdout or "<-" in stdout
    print("PASS: view shows connections")


def test_slugify_is_correct():
    """Test that node IDs use properly slugified headers."""
    code, stdout, stderr = run(["headers", "--file", "embeddings.md", "--all"])
    assert code == 0
    assert "positional-bias" in stdout
    assert "token-budget" in stdout
    print("PASS: slugify produces correct node IDs")


def test_graph_depth_traversal():
    """Test that graph depth traversal works."""
    code, stdout, stderr = run(["graph", "--header", "Attention Limits", "--depth", "3"])
    assert code == 0
    assert "Embedding Capacity" in stdout
    print("PASS: graph depth traversal works")


def test_integration():
    """Integration test with temp directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        docs = Path(tmpdir) / "docs"
        docs.mkdir()
        
        (docs / "test.md").write_text("""## First Concept

See [Second Concept](./test.md#second-concept).

---

## Second Concept

Related to [First Concept](#first-concept).
""")
        
        result = subprocess.run(
            ["python3", "src/mem_graph.py", "--root", str(docs), "check"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, f"Expected OK but got: {result.stderr}"
        assert "OK" in result.stdout
        print("PASS: integration test")


if __name__ == "__main__":
    tests = [
        test_heading_level_2_is_node,
        test_level_1_heading_not_node,
        test_check_passes_after_heading_fix,
        test_inline_code_links_ignored,
        test_graph_file_and_header_disambiguation,
        test_graph_ambiguous_shows_error,
        test_nonexistent_shows_similar_suggestions,
        test_errors_go_to_stderr,
        test_check_output_has_line_numbers,
        test_view_nonexistent_shows_helpful_message,
        test_view_shows_connections,
        test_slugify_is_correct,
        test_graph_depth_traversal,
        test_integration,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"FAIL: {test.__name__} - {e}")
            failed += 1
    
    print(f"\n{len(tests) - failed}/{len(tests)} tests passed")
    sys.exit(failed)
