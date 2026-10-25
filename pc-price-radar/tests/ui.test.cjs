/* Browser-side smoke checks without network, npm or fragile selectors. */
"use strict";
const fs = require("node:fs");
const vm = require("node:vm");
const assert = require("node:assert/strict");
const path = require("node:path");

const root = path.resolve(__dirname, "..");
const html = fs.readFileSync(path.join(root, "index.html"), "utf8");
const match = html.match(/<script>([\s\S]+?)<\/script>/);
assert(match, "A browser script must exist");
new vm.Script(match[1], {filename: "index.html inline script"});

const tabs = ["stores", "offers", "deals", "add", "guide"];
for (const tab of tabs) {
  assert(html.includes('data-tab="' + tab + '"'), "Tab not found: " + tab);
  assert(html.includes('id="' + tab + 'Tab"'), "Panel not found: " + tab);
}
for (const file of ["catalog.json", "offers.json", "deals.json", "price-history.json", "sources-status.json"]) {
  assert(html.includes('./' + file), "Missing data endpoint: " + file);
  JSON.parse(fs.readFileSync(path.join(root, file), "utf8"));
}
const catalog = JSON.parse(fs.readFileSync(path.join(root, "catalog.json"), "utf8")).sources;
assert(catalog.length >= 200, "The candidate-source inventory should have 200+ domains");
assert.equal(new Set(catalog.map(x => x.domain)).size, catalog.length, "Duplicate source domains");
assert(catalog.every(x => x.catalog_status === "PENDIENTE_VALIDACION"), "Candidate is falsely audited");

const m = match[1].match(/function price\(o\)\{([\s\S]*?)\}\s*function score/);
assert(m, "Price calculator not found");
const price = new Function("o", m[1]);
const offer = {price: 5_000_000, discount: 10, shipping: 100_000, taxes: 0,
               coupon: 300_000, fx: 1, coupon_status: "unconfirmed"};
assert.equal(price(offer), 4_600_000, "Unconfirmed coupon MUST NOT reduce total");
assert.equal(price({...offer, coupon_status: "checkout_verified"}), 4_300_000);
assert.equal(price({...offer, discount: 0, coupon: 0, shipping: null, taxes: null}), 5_000_000);
console.log("UI syntax, tab wiring, source integrity and coupon totals: OK", catalog.length);
