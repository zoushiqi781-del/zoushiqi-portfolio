import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Static export → plain HTML/CSS/JS in `out/`, hostable on any static server
  // (used to self-host on a China-accessible VPS instead of Vercel).
  output: "export",
  images: {
    // the static export has no image optimizer, so serve images as-is
    unoptimized: true,
  },
};

export default nextConfig;
