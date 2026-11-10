export function discount(total, isMember) {
  if (total <= 0) {
    return 0;
  }
  const rate = isMember ? 0.1 : 0;
  return Math.round(total * (1 - rate) * 100) / 100;
}
