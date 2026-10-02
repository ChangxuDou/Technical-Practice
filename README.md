# Technical Projects & Portfolio

A collection of deployed projects, database designs and programming exercises by **Changxu Dou (Ryandou)**, an IT Product Manager developing practical skills in Python, Django and SQL.

This repository documents my progression from learning programming fundamentals to connecting business requirements, data models and application workflows in a working web application.

## Featured Project — Vidly

**Vidly** is a deployed movie-disc rental prototype covering customer, cashier and manager workflows.

The application supports rentals and returns, inventory management, customer wishlists, procurement and stock receiving, simulated wallet top-ups, rewards, coupons and operational reporting.

I built the initial application through self-directed learning, then extended and refined it with AI assistance. My work included requirements definition, relational database modelling, business-rule validation and deployment to PythonAnywhere.

**Technology:** Python · Django · SQLite · HTML · CSS · JavaScript

**[Explore the Live Demo](https://ryandou.pythonanywhere.com/) · [Project Background & Q&A](https://ryandou.pythonanywhere.com/qa/)**

The demo uses simulated payments and is intended for portfolio presentation and learning.

## Demo Accounts & Role Permissions

Explore the application from three perspectives: customer, cashier and store manager.

**Shared demo password:** `VidlyDemo!2026`

| Username | Role | What you can do |
|---|---|---|
| `demo` | Customer | Browse and search movies, add available titles to the rental bag, submit rentals and view your own rental history. Submit movie requests to the wishlist and track their progress. Simulate wallet top-ups, view your balance and points history, and claim available coupons. Returns are handled by store staff. |
| `cashier` | Cashier | Manage customer records, process counter rentals using movie barcodes, and handle full or partial returns, lost-disc charges and settlement. Apply eligible customer coupons, manage customer wallet top-ups and refunds, and receive deliveries against purchase orders to update inventory. |
| `manager` | Store Manager | Access all cashier functions, maintain the movie catalogue, manage stock and rental prices, review aggregated wishlist demand, and create purchase orders. Configure coupons and top-up reward rules, and view reports on revenue, popular movies and leading customers. |

### Suggested Demo Journey

1. **As a customer:** browse the catalogue, rent a movie, submit a wishlist request, and try a simulated wallet top-up.
2. **As a cashier:** find the customer’s rental and process a return or partial return.
3. **As a manager:** review wishlist demand, create a purchase order, receive stock, and explore reward settings and reports.

### Demo Scope

Vidly is a portfolio project modelling a **physical movie-disc rental store**. Payments and procurement are simulated; no real money is charged and no supplier orders are placed.

These are shared accounts, so activity may be visible to other visitors. Please use fictional information when exploring the application.

## Explore This Repository

- **[Python](./Python/)** — Django application work, Python exercises and data-processing practice.
- **[SQL](./SQL/)** — Relational database designs and SQL practice, including movie rental and flight booking scenarios.

The exercises document the foundations behind my project work; the deployed application demonstrates how I apply those foundations to connected business workflows.
