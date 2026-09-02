import os
import subprocess
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
INIT = os.path.join(HERE, "wf-init.sh")


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(text)
    return p


class MarkerScopeTest(unittest.TestCase):
    """insert_fragment() 只該在合法能持有 marker 的檔案裡找，
    不該被 examples/ 之類同文件名＋同 marker 的誘餌檔誤中。"""

    def setUp(self):
        self.d = tempfile.TemporaryDirectory()
        self.root = self.d.name

    def tearDown(self):
        self.d.cleanup()

    def test_decoy_marker_in_examples_is_not_matched(self):
        write(
            self.root,
            "examples/dev-minimal/WORKFLOWS.md",
            "decoy\n<!-- wf-insert:WORKFLOWS -->\n",
        )
        r = subprocess.run(
            ["bash", INIT, "--target", self.root, "--flavor", "dev",
             "--non-invasive", "wf", "--quiet"],
            capture_output=True, text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)

        decoy = os.path.join(self.root, "examples/dev-minimal/WORKFLOWS.md")
        with open(decoy, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "decoy\n<!-- wf-insert:WORKFLOWS -->\n")

        real = os.path.join(self.root, "wf/WORKFLOWS.md")
        with open(real, encoding="utf-8") as fh:
            body = fh.read()
        self.assertIn("feature-dev", body)
        self.assertIn("dev-env", body)


if __name__ == "__main__":
    unittest.main()
