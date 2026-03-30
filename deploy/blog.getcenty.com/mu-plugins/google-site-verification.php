<?php
/**
 * Plugin Name: Google Search Console verification
 * Description: HTML tag for blog.getcenty.com URL-prefix property in Search Console.
 */
declare(strict_types=1);

add_action(
    'wp_head',
    static function (): void {
        echo '<meta name="google-site-verification" content="VkTLd6XDqqgcxUpB9gDzGam55mWksAkbo8g1WKmQTbA" />' . "\n";
    },
    1
);
