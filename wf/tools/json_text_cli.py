"""json_text_cli — json_text.py 的 HELP 與 --setup 那段（git、interpreter、setup），從上游原樣搬出來，只多了參數。

來源：aos repo 的 wf/tools/json_text.py（repo-aos commit b374ac376）。拆出來只為了本 repo 單檔 ≤ 8192 bytes；
差別：setup() 多收 script（json_text.py 的絕對路徑，原本用 __file__）、write、fail（原本是同檔的函式）。
"""
import os
import subprocess

KEY = "diff.json_text.textconv"
HELP = """json_text - expand a JSON file into line-oriented text for humans and for git diff (textconv).

usage: json_text.py [--md] FILE
       json_text.py --setup [--check]
  FILE      the JSON file; output goes to stdout as UTF-8
  --md      print a simple Markdown view instead (one section per string)
  --setup   set diff.json_text.textconv in the .git/config of the repo this
            script lives in (safe to rerun; prints the current state)
  --check   with --setup: only look; exit 0 if set as expected, 1 if not
  --help    show this help

Default output, in document order (keys are not sorted):
  #/a/b            a string node: a header line (JSON Pointer), then the content;
    line one       each content line is indented by two spaces; long lines are
    ↪ next one      folded after sentence ends, folded lines start with '↪ '
  #/n = 3          numbers (as written), true/false/null, "", {}, []
  #/list/-/name    array elements are written as '-', never as an index, so
                   inserting an element does not change the lines after it
  #/x = {"$ref": "a.json"}   objects with a '$' key are printed on one line
Control characters other than tab are shown as \\u000d etc.
If FILE is not valid JSON (or not UTF-8), a warning goes to stderr, the raw text
is printed unchanged and the exit code is 0, so git falls back to a plain diff.

git: put 'PATTERN diff=json_text' in .gitattributes, then once per clone run
  python3 wf/tools/json_text.py --setup      (or: python ... on Windows)
"""


def git(top, *args):
    return subprocess.run(["git", "-C", top] + list(args), capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def interpreter():
    """The name of a Python 3 on PATH, as it should appear in the git config ('python3' or 'python')."""
    for name in ("python3", "python"):
        try:
            r = subprocess.run([name, "-c", "import sys; sys.exit(sys.version_info[0] != 3)"], capture_output=True)
        except OSError:
            continue
        if r.returncode == 0:
            return name
    return None


def setup(check, script, write, fail):
    here = os.path.dirname(script)
    r = git(here, "rev-parse", "--show-toplevel")
    if r.returncode != 0:
        fail("NotInRepo %s is not inside a git work tree" % here)
        return 1
    top = r.stdout.strip()
    rel = os.path.relpath(script, os.path.abspath(top)).replace(os.sep, "/")
    name = interpreter()
    if name is None:
        fail("PythonMissing neither python3 nor python on PATH runs Python 3")
        return 1
    want = '%s -B "%s"' % (name, rel) if " " in rel else "%s -B %s" % (name, rel)
    now = git(top, "config", "--local", "--get", KEY).stdout.strip()
    used = git(top, "ls-files", ":(attr:diff=json_text)").stdout.split("\n")
    note = "%d tracked files use diff=json_text" % len([u for u in used if u])
    if now == want:
        write("%s = %s (already set; %s)\n" % (KEY, want, note))
        return 0
    if check:
        write("%s is %s, expected %s (%s)\n" % (KEY, repr(now) if now else "not set", want, note))
        return 1
    r = git(top, "config", "--local", KEY, want)
    if r.returncode != 0:
        fail("ConfigFailed git config: %s" % r.stderr.strip())
        return 1
    write("%s = %s (was %s; %s)\n" % (KEY, want, repr(now) if now else "not set", note))
    return 0
