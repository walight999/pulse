import { test, expect } from "@playwright/test";

const DASHBOARD_URL = process.env.PULSE_DASHBOARD_URL || "http://localhost:8501";

test.describe("Dashboard", () => {
  test("page title set to brand", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await expect(page).toHaveTitle(/pulse/i);
  });

  test("sidebar brand row shows P + wordmark", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    const brandRow = page.locator(".pulse-brand-row").first();
    await expect(brandRow).toBeVisible();
    // Wordmark must be lowercase "pulse"
    await expect(brandRow.locator(".pulse-brand-name")).toContainText("pulse");
  });

  test("logo is inline SVG (not CSS pseudo) — regression test", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    const logoSvg = page.locator(".pulse-logo-mark svg").first();
    await expect(logoSvg).toBeVisible();
  });

  test("sidebar nav has all 4 main items", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    for (const label of ["Overview", "Subscriptions", "Activity", "AI usage"]) {
      await expect(page.locator(`button:has-text("${label}")`).first()).toBeVisible();
    }
  });

  test("overview shows ECG line", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    const ecg = page.locator(".pulse-ecg-line").first();
    // ECG line is on Overview by default
    await expect(ecg).toBeVisible({ timeout: 8_000 });
  });

  test("settings has exactly 3 tabs (Advanced removed)", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    await page.locator('button:has-text("Settings")').first().click();
    await page.waitForTimeout(500);
    // Streamlit tabs render as buttons with role=tab
    const tabs = page.locator('[role="tab"]');
    const count = await tabs.count();
    expect(count).toBe(3);
    await expect(tabs.nth(0)).toContainText(/Preferences/i);
    await expect(tabs.nth(1)).toContainText(/Pulse Pro/i);
    await expect(tabs.nth(2)).toContainText(/Data/i);
  });

  test("no Streamlit branding visible", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    // Deploy button should be hidden
    const deployBtn = page.locator('[data-testid="stDeployButton"]');
    await expect(deployBtn).toHaveCount(0).catch(async () => {
      // Or it exists but visibility:hidden — check that:
      const visible = await deployBtn.first().isVisible().catch(() => false);
      expect(visible).toBe(false);
    });
  });

  test("AI usage page renders without crash", async ({ page }) => {
    await page.goto(DASHBOARD_URL);
    await page.waitForLoadState("networkidle");
    await page.locator('button:has-text("AI usage")').first().click();
    await page.waitForTimeout(1_500);
    // Either ROI hero or empty state should be visible
    const hasContent = await page.locator(
      'text=/return on plan cost|No AI usage in this range/i'
    ).first().isVisible({ timeout: 5_000 }).catch(() => false);
    expect(hasContent).toBe(true);
  });
});
