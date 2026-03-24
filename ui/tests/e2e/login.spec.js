const { test, expect } = require('@playwright/test');

test.describe('Login Flow', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    // Go to the login page
    await page.goto('/login');

    // Check if we are on the login page
    await expect(page).toHaveTitle(/Login/);

    await page.locator('input[placeholder="Username"]').fill('testuser');
    await page.locator('.p-password-input').fill('password123');

    // Click the login button
    await page.click('input[type="submit"]');

    // Verify that we are redirected (e.g., to the home page or portfolio list)
    // Nuxt auth usually redirects to '/' by default
    await expect(page).toHaveURL(/\/$/);
    
    // Check for some element that should be visible after login
    // e.g., a logout button or user info
    // Based on UserView, it returns username, etc.
    // Let's just check if the URL is correct for now as a baseline.
  });

  test('should show error message with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[placeholder="Username"]', 'wronguser');
    await page.fill('input[placeholder="Password"]', 'wrongpass');
    await page.click('input[type="submit"]');

    // Check for error message
    // The component has .p-error
    const errorMsg = page.locator('.p-error');
    await expect(errorMsg).not.toHaveClass(/invisible/);
    await expect(errorMsg).toBeVisible();
  });
});
