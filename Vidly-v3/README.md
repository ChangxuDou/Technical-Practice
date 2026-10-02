# Vidly v3 — English edition with project Q&A

A personal learning project by **Ryandou**, a product manager connecting Python/Django, database modelling and product workflows. The first working platform was subsequently refined with AI.

Vidly demonstrates a physical movie-disc rental store, not a streaming service. All payments and supplier purchases are simulated.

## Start locally

Requires Python 3.10 or newer. Extract the ZIP, open a terminal in its folder, and run:

```sh
bash Start.command
```

The launcher creates a local virtual environment, installs the pinned dependencies, applies database migrations and starts the app at http://127.0.0.1:8000/ . An internet connection is needed for the first dependency installation.

For another port:

```sh
PORT=8001 bash Start.command
```

| Account | Role | Password |
|---|---|---|
| demo | Customer | VidlyDemo!2026 |
| cashier | Cashier | VidlyDemo!2026 |
| manager | Manager | VidlyDemo!2026 |

These accounts are for local demonstration only. The manager is not a superuser. To create your own administrator after setup:

```sh
.venv/bin/python manage.py createsuperuser
```

## New in v3

- **Q&A** in the main navigation, footer and homepage. Fifteen expandable questions explain the project background, rental journey, role permissions, wishlist-to-stock flow, coupons, top-ups, rewards and reports. No login is required.
- English customer and staff pages, forms, validation messages, status labels, administrative labels, confirmations and built-in movie descriptions.
- English layouts checked on desktop and a 390px mobile viewport.
- Upgrade migration converts known demo text and old staff group names while retaining membership and permissions. Arbitrary user-authored names, notes and descriptions are preserved as entered.

## Explore the business flow

1. Sign in as `demo`, choose a movie and confirm a rental from the bag. Time starts immediately and available stock decreases.
2. Review the rental. Customers cannot process returns themselves.
3. Sign in as `cashier`, open **Staff desk**, select the rental and record normal returns or lost copies. Partial returns are supported.
4. Settle using simulated cash or available wallet balance. Apply a valid claimed coupon to rental fees if desired.
5. Normal returns restore available stock; lost copies reduce total stock. Reports record the settled revenue.

**Missing movies:** customer submits a Wishlist request → manager reviews aggregated demand → manager creates a purchase order → manager or cashier receives the physical copies → stock and wishlist progress update. Purchase orders alone do not increase stock.

**Wallet:** customer creates a top-up → local simulator chooses success, failure or cancellation → success credits balance and points once. Repeated submission does not credit twice. No real payment service is called.

**Coupons:** customers enter a code in My rentals. The clean demo includes `WELCOME10` (10% off rent). Managers configure coupon codes, percentages and expiry through **Manage coupons** in the staff navigation.

**Rewards:** managers and superusers configure points per EUR and can pause new top-ups. Points are calculated proportionally, rounded down, using a policy snapshot valid for 30 minutes. Points are displayed only, not redeemed against rent. Staff-entered top-ups and rental spending do not earn additional points. Balance refunds reverse original top-up rewards proportionally.

**Reports:** daily, monthly and yearly settlement revenue, total rental orders, popular movies and top customers. Revenue includes lost-disc charges and subtracts coupon discounts; top-ups are excluded. Reporting time zone: Europe/Berlin.

## Upgrade an existing enhanced v1 or v2 installation

1. Stop the old server and back up its entire folder, especially `db.sqlite3`.
2. Extract v3 into a separate folder.
3. Replace the extracted v3 `db.sqlite3` with a copy of your enhanced v1/v2 database.
4. Run `bash Start.command`. Migrations retain customers, orders, balances, points, inventory and staff permissions. Existing movie data is not re-seeded on startup.

Do not use the original course Django 2.1 database directly with this release. The upgrade path above is for the enhanced Django 5.2 editions. Keep the original folder for rollback; English data conversions are not automatically reversed.

The ZIP includes a **clean demo database** with 14 movies, 9 genres and 124 available copies, three demo accounts and no rental/payment history. The running local preview may contain your earlier test activity and therefore show different totals.

## Checks

```sh
.venv/bin/python manage.py test rentals movies
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations --check --dry-run
```

See `docs/TEST_REPORT.md` for verification details and `docs/CHANGELOG_V3.md` for this update.

## Scope and deployment

This is a local demonstration. It does not connect to banks, suppliers or real payments; stream films; ship discs; redeem points; or track disc collection as a separate action. The SQLite database is suitable for local exploration; production load testing and a production security review have not been performed.

For a real deployment, configure `DJANGO_DEBUG=0`, a new `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` and HTTPS settings including `DJANGO_CSRF_ORIGINS`. Replace demo accounts, run `collectstatic`, and use the included Gunicorn/WhiteNoise setup behind an HTTPS proxy. `VIDLY_DB` can point to a separate database file. This release has not been published to a public hosting service.
