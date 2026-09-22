# Architecture

The content script reads bounded visible text only, debounces DOM changes, and sends a message to the MV3 service worker. The worker prevents duplicate scans, applies local safety rules/ML API, records anonymous local totals, and navigates only the affected tab to the extension-owned block page. The backend never writes request content to disk.
