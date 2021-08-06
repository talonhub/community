mocha test block:
  "describe('', () => {"
  key(enter)
  key(tab)
    "it('', () => {"
    key(enter)
    key(tab:2)
      "// setup"
      key(enter:2)
      "// exercise"
      key(enter:2)
      "// verify"
      key(enter:2)
      "assert.strictEqual()"
      key(enter:2)
    "})"
    key(enter)
    "});"
    key(up:11)
    key(right:3)

mocha it block:
    "it('', () => {"
    key(enter)
    key(tab:2)
      "// setup"
      key(enter:2)
      "// exercise"
      key(enter:2)
      "// verify"
      key(enter:2)
      "assert.strictEqual()"
      key(enter:2)
    "})"
    key(up:9)
    key(left:4)


