export function price(base, quantity) {
  if (quantity < 1) {
    throw new RangeError("quantity must be at least 1");
  }
  return base * quantity;
}
