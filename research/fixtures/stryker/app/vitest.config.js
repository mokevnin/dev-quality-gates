import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["test/**/*.test.js"],
    // Fails a test that makes no assertion, so the weak case below has to assert something.
    expect: { requireAssertions: true },
    coverage: {
      provider: "v8",
      include: ["src/**/*.js"],
      reporter: ["lcov", "cobertura", "text-summary"],
    },
  },
});
