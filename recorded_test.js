import { test, expect } from '@playwright/test';

test('test', async ({ page }) => {
  await page.goto('https://www.google.com/');
  await page.getByRole('combobox', { name: 'Search' }).click();
  await page.getByRole('link', { name: 'Sign in' }).click();
  await page.getByRole('textbox', { name: 'Email or phone' }).click();
  await page.getByRole('textbox', { name: 'Email or phone' }).fill('qwe');
  await page.getByRole('button', { name: 'Next' }).click();
  await page.getByRole('button', { name: 'Create account' }).click();
  await page.getByRole('menu', { name: 'Create account' }).click();
  await page.getByRole('button', { name: 'Yes, continue' }).click();
});