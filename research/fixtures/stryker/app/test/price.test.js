import { expect, it } from "vitest";
import { price } from "../src/price.js";

it("multiplies base by quantity", () => {
  expect(price(5, 3)).toBe(15);
  expect(price(5, 1)).toBe(5);
});

it("rejects a quantity below one", () => {
  expect(() => price(5, 0)).toThrow(RangeError);
});
