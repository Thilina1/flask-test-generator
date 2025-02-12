import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://flutter.dev/');
  await page.locator('#get-started__header').click();
  await page.getByRole('link', { name: 'macOS' }).click();
});