# v3 — Project Q&A and English interface

- Added a public `/qa/` page with fifteen native, keyboard-accessible expandable answers in four topic groups.
- Described Ryandou as a product manager who self-studied Python, backend development and database modelling, built an initial working platform, and then improved it with AI.
- Documented the physical disc rental scenario, rental timing, staff-only returns, losses, partial returns, wishlist demand, purchases, receiving, coupons, wallet top-ups, reward policy and performance reporting.
- Added Q&A entry points to the header, homepage and footer; footer credits Ryandou.
- Converted customer pages, staff workflows, administrative forms, built-in validation and custom business messages to English. Django uses `en-gb`.
- Translated the built-in catalog descriptions and known demo records through a migration. Custom user-authored content is retained unchanged.
- Converted old Chinese staff group names to Manager and Cashier while preserving permissions and membership, including safe merging when English groups already exist.
- Adjusted navigation and text layout for longer English labels on desktop and mobile.
- Retained all v2 business rules and the clean-database ZIP delivery approach.
