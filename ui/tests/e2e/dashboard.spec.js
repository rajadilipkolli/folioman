const { test, expect } = require('@playwright/test');

test.describe('Dashboard Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test in this describe block
    await page.goto('/login');
    await page.locator('input[placeholder="Username"]').fill('testuser');
    await page.locator('.p-password-input').fill('password123');
    await page.click('input[type="submit"]');
    await expect(page).toHaveURL(/\/$/);
  });

  test('should display dashboard components', async ({ page }) => {
    // Check for "Current Value" card
    await expect(page.locator('text=Current Value')).toBeVisible();
    
    // Check for "Portfolio Performance" section
    await expect(page.locator('text=Portfolio Performance')).toBeVisible();

    // Check for sidebar items
    await expect(page.getByText('Current Value')).toBeVisible();
    await expect(page.getByText('Portfolio Performance')).toBeVisible();
    await expect(page.locator('text=Analysis')).toBeVisible();
    await expect(page.locator('text=Import Portfolio')).toBeVisible();
  });

  test('should allow navigating to Portfolio page', async ({ page }) => {
    await page.click('text=Portfolio');
    // Verify redirection to portfolio page (link goes to /mutualfunds/schemes)
    await expect(page).toHaveURL(/.*mutualfunds/);
  });
});
