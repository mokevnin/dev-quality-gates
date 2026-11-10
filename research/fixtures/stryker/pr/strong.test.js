import { expect, it } from "vitest";
import { discount } from "../src/discount.js";

it("takes ten percent off for members", () => {
  expect(discount(100, true)).toBe(90);
  expect(discount(19.99, true)).toBe(17.99);
});

it("charges the full total to non-members", () => {
  expect(discount(100, false)).toBe(100);
});

it("returns zero for an empty or negative total", () => {
  expect(discount(0, true)).toBe(0);
  expect(discount(-5, true)).toBe(0);
  expect(discount(0.01, false)).toBe(0.01);
});
