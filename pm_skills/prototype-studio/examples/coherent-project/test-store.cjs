/* Same persisted fixture viewed through independent page contexts. No real business data. */
const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const source = fs.readFileSync(__dirname + "/prototype/store.js", "utf8");
const persisted = new Map();
let uuid = 0;
function page() {
  const window = {dispatchEvent() {}, crypto: {randomUUID: () => "test-" + (++uuid)}};
  const context = {window, localStorage: {getItem: key => persisted.get(key) ?? null, setItem: (key, value) => persisted.set(key, value)}, Event: class Event {}};
  vm.runInNewContext(source, context);
  return window.FixtureStore;
}
const records = page(), summary = page();
const totals = () => JSON.parse(JSON.stringify(summary.stats()));
assert.deepEqual(totals(), {total: 3, open: 2, done: 1});
records.create(" New cross-page record ");
assert.deepEqual(totals(), {total: 4, open: 3, done: 1});
const added = summary.all().find(row => row.id === "test-1");
assert.equal(added.title, "New cross-page record");
records.update(added.id, "Changed title");
assert.equal(summary.all().find(row => row.id === added.id).title, "Changed title");
records.toggle(added.id);
assert.deepEqual(totals(), {total: 4, open: 2, done: 2});
assert.throws(() => records.create("   "), /标题/);
assert.deepEqual(totals(), {total: 4, open: 2, done: 2});
records.remove(added.id);
assert.deepEqual(totals(), {total: 3, open: 2, done: 1});
assert.equal(summary.all().some(row => row.id === added.id), false);
records.reset();
assert.deepEqual(totals(), {total: 3, open: 2, done: 1});
console.log("PASS: independent page contexts share CRUD records and derived statistics");
