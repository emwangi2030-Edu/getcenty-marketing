# blog.getcenty.com — Search Console verification

## HTML tag (primary)

The active site outputs this in `<head>` via **must-use plugin**:

`wp-content/mu-plugins/google-site-verification.php`

Token: `VkTLd6XDqqgcxUpB9gDzGam55mWksAkbo8g1WKmQTbA` (matches GSC → HTML tag method).

After updating that file on the server, purge **LiteSpeed Cache** (or wait for TTL), then click **Verify** in Search Console.

## HTML file (alternate)

If you use Google’s **HTML file upload** method instead, copy `google4df65b10c57911b3.html` to the WordPress **document root** (same folder as `wp-config.php`), so it is reachable at:

`https://blog.getcenty.com/google4df65b10c57911b3.html`

Do **not** use both methods unless GSC asks for it; one successful verification is enough.

## Child theme (optional)

You can move this tag into the active theme’s `functions.php` and **delete** this MU-plugin. Do not output the same meta in both places.
