# WordPress publish pipeline

Publishes a blog pillar draft from `docs/blog-content/<slug>.html` to `blog.getcenty.com` via the WordPress REST API, triggered from GitHub Actions.

**Safety defaults you should not relax casually:**

- New posts land as **`draft`**. A human reviews in WP admin (featured image, Rank Math meta, statutory check) and flips to publish.
- **`dry_run=true`** is the default for `workflow_dispatch`. Nothing writes to WP unless you set it to `false`.
- **`update_if_exists=false`** is the default. A duplicate slug fails loudly rather than silently overwriting.

## One-time setup

### 1. Create a WordPress Application Password

In `blog.getcenty.com` WP admin → **Users → Edit Profile** for a user with `edit_posts` and `publish_posts` capabilities → **Application Passwords** → name it `github-actions-publish` → **Add New Application Password**.

Copy the generated password (spaces are cosmetic; the script strips them).

### 2. Add repository secrets

GitHub → **Settings → Secrets and variables → Actions → New repository secret**:

| Name | Value |
|------|-------|
| `WP_BLOG_URL` | `https://blog.getcenty.com` |
| `WP_BLOG_USER` | username from step 1 |
| `WP_BLOG_APP_PASSWORD` | application password from step 1 |

### 3. (Recommended) Install the Rank Math REST shim

Rank Math stores SEO meta in standard `wp_postmeta` but does not register most of its keys for the REST API by default. The publish script will send `rank_math_title`, `rank_math_description`, and `rank_math_focus_keyword` in the post payload; without the shim below, those values are accepted but not echoed back and the WP admin sidebar may still show empty Rank Math fields until you re-enter them manually.

Drop this file into `wp-content/mu-plugins/expose-rank-math-rest.php` on the server:

```php
<?php
/**
 * Plugin Name: Expose Rank Math meta to REST
 * Description: Allow the WP REST API to read/write Rank Math title, description, and focus keyword from authenticated requests with edit_post capability.
 */
add_action( 'init', function () {
    $keys = [ 'rank_math_title', 'rank_math_description', 'rank_math_focus_keyword' ];
    foreach ( $keys as $key ) {
        register_post_meta( 'post', $key, [
            'show_in_rest'  => true,
            'single'        => true,
            'type'          => 'string',
            'auth_callback' => function () { return current_user_can( 'edit_posts' ); },
        ] );
    }
} );
```

Without this shim, the workflow still creates the post correctly — you just have to set Rank Math meta manually in the WP admin sidebar after the workflow finishes.

### 4. Create blog categories (if needed)

The script does **not** auto-create categories. Ensure the categories named in each sidecar JSON (`category_slugs`) exist in WP admin before publishing.

## Sidecar metadata

Each pillar HTML must have a matching JSON sidecar in the same folder:

```
docs/blog-content/002-casual-workers-payments-kenya.html
docs/blog-content/002-casual-workers-payments-kenya.json
```

Required fields (script fails fast if missing):

| Field | Purpose |
|-------|---------|
| `title` | WP post title |
| `slug` | WP post slug (the URL segment) |
| `excerpt` | WP excerpt + fallback meta description |
| `focus_keyword` | Rank Math focus keyword |

Optional fields:

| Field | Purpose |
|-------|---------|
| `meta_title` | Rank Math SEO title (falls back to `title`) |
| `meta_description` | Rank Math meta description (falls back to `excerpt`) |
| `category_slugs` | Array of existing WP category slugs to assign |

Featured images are intentionally **not** in the sidecar — set them in WP admin so the media library reflects the licence and alt text consciously.

## Triggering a publish

GitHub → **Actions → "WP — publish blog draft" → Run workflow**:

| Input | Default | Meaning |
|-------|---------|---------|
| `slug` | (required) | File slug without extension, e.g. `002-casual-workers-payments-kenya` |
| `status` | `draft` | Initial WP post status |
| `update_if_exists` | `false` | Update an existing post with the same slug instead of failing |
| `dry_run` | `true` | Validate inputs and load files but do not write to WP |

### First run for a new pillar

1. Run with defaults (`status=draft`, `dry_run=true`) to validate sidecar + HTML are loadable.
2. Re-run with `dry_run=false`, `status=draft` — creates a draft post in WP.
3. Open the post in WP admin. Set featured image, confirm Rank Math meta, run the Publishing DOD checklist in `docs/SEO-GOVERNANCE.md`.
4. Flip status to **Publish** in WP admin.
5. Update `docs/SEO-KEYWORD-MAP.csv` row to `status=live`, add the URL to `docs/seo-check-urls.txt`, and trigger the `ping` job in `seo-automation.yml`.

### Updating an existing pillar

Run with `update_if_exists=true`, `dry_run=false`. The script matches by slug; multiple matches abort.

### Why not direct publish?

The `status=publish` option exists for cases where the draft has already been reviewed (for example a re-publish after a refresh). For first-time publish of any new pillar, **always go through draft** so the statutory + featured image + Rank Math review is impossible to skip.

## Failure modes the script catches

- Missing sidecar JSON or HTML file.
- Sidecar missing required field (`title`, `slug`, `excerpt`, `focus_keyword`).
- WP credentials missing.
- Status not in `{draft, publish}`.
- Duplicate post by slug without `update_if_exists=true`.
- Unknown category slug.
- Multiple WP posts with the same slug (refuses to guess).
- Non-2xx response from WP REST.

## What this pipeline does NOT do

- Upload featured images (manual in WP admin).
- Purge LiteSpeed cache (configure separately; usually a server-side cron or the LiteSpeed REST endpoint with a per-site token).
- Set Yoast / All-in-One SEO meta (we use Rank Math).
- Auto-create WP categories or tags.
- Manage redirects.
- Replace placeholder spoke anchors in the HTML — those are content edits, not pipeline edits.
