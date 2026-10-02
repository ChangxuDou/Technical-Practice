# Vidly v3 verification

## Automated coverage

74 Django tests pass: the 70 existing business tests plus four English/Q&A upgrade checks.

New checks cover public Q&A content and links; rendered English pages for guests, customers, cashiers and managers including Django administration; English authentication and form errors; and idempotent legacy group/data translation that preserves custom descriptions, balances, points, inventory and permissions.

Existing checks cover staff-only returns, ownership, stock limits, partial returns and losses, settlement, coupons, wallet refunds, wishlist deduplication, procurement, receiving, top-up idempotency, policy snapshots, simulated payment outcomes, and role permissions.

## Visual / interaction checks

- Desktop homepage and Q&A rendering.
- Q&A expands with a click and collapses with the Enter key.
- English homepage and Q&A at a 390 × 844 viewport: no horizontal page overflow.
- Existing staff overview and rental data render in English after migration.

## Release checks

- Fresh migrations, clean demo seeding, Django system checks and collected static assets.
- No pending model migrations.
- DEBUG=0 page smoke checks with a temporary secret.
- ZIP integrity and extracted-package tests.
- Clean release database contains no personal rental or payment activity.

This does not constitute a production security audit, real payment integration test or concurrent load test.
