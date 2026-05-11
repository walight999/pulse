import { test, expect } from "@playwright/test";

const LANDING_URL = process.env.PULSE_LANDING_URL || "http://localhost:3000";

test.describe("Landing page", () => {
  test("loads with brand identity", async ({ page }) => {
    const start = Date.now();
    await page.goto(LANDING_URL);
    await expect(page).toHaveTitle(/pulse.*Mint for the AI era/i);
    expect(Date.now() - start).toBeLessThan(8_000);
  });

  test("hero shows specific savings number", async ({ page }) => {
    await page.goto(LANDING_URL);
    await expect(page.locator("h1")).toContainText(/\$200/);
    await expect(page.locator("h1")).toContainText(/\$4,000/);
  });

  test("nav links present", async ({ page }) => {
    await page.goto(LANDING_URL);
    await expect(page.getByRole("link", { name: /features/i })).toBeVisible();
    await expect(page.getByRole("link", { name: /pricing/i })).toBeVisible();
    await expect(page.getByRole("link", { name: /github/i })).toBeVisible();
  });

  test("compare table mentions competitors", async ({ page }) => {
    await page.goto(LANDING_URL);
    await expect(page.locator("text=ClaudeMetrics").first()).toBeVisible();
    await expect(page.locator("text=Anthropic Console").first()).toBeVisible();
  });

  test("pricing shows 4 tiers", async ({ page }) => {
    await page.goto(LANDING_URL);
    await expect(page.locator("text=/^Free$/").first()).toBeVisible();
    await expect(page.locator("text=/^Pro$/").first()).toBeVisible();
    await expect(page.locator("text=/^Team$/").first()).toBeVisible();
    await expect(page.locator("text=/^Enterprise$/").first()).toBeVisible();
  });

  test("waitlist form validates", async ({ page }) => {
    await page.goto(LANDING_URL);
    const emailInput = page.locator('input[type="email"]').first();
    await emailInput.fill("not-an-email");
    const submit = page.getByRole("button", { name: /join waitlist|notify me/i }).first();
    await submit.click();
    // Should show validation (either browser-native or app-level)
    const isInvalid = await emailInput.evaluate(
      (e: HTMLInputElement) => !e.checkValidity()
    );
    expect(isInvalid).toBe(true);
  });

  test("OG card meta is set", async ({ page }) => {
    await page.goto(LANDING_URL);
    const ogImage = await page.locator('meta[property="og:image"]').getAttribute("content");
    expect(ogImage).toBeTruthy();
    expect(ogImage).toMatch(/og-social-card|brand/);
  });

  test("favicon present", async ({ page }) => {
    await page.goto(LANDING_URL);
    const favicon = await page.locator('link[rel="icon"]').first().getAttribute("href");
    expect(favicon).toBeTruthy();
  });

  test("ECG line animation rendered", async ({ page }) => {
    await page.goto(LANDING_URL);
    const ecg = page.locator(".ecg-line").first();
    await expect(ecg).toBeVisible();
  });
});
