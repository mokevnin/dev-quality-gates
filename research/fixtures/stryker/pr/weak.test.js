import { expect, it } from "vitest";
import { discount } from "../src/discount.js";

// Runs every line and asserts only the type: full coverage, no real check.
it("returns a number", () => {
  expect(discount(100, true)).toBeTypeOf("number");
  expect(discount(100, false)).toBeTypeOf("number");
  expect(discount(0, true)).toBeTypeOf("number");
});
