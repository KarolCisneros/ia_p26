/**
 * Eleventy Configuration for uu_framework
 * Static site generator for ITAM course materials
 */

const markdownIt = require("markdown-it");
const markdownItContainer = require("markdown-it-container");
const markdownItAttrs = require("markdown-it-attrs");
const markdownItAnchor = require("markdown-it-anchor");

module.exports = function(eleventyConfig) {

  // ============================================
  // Markdown Configuration
  // ============================================

  const mdOptions = {
    html: true,
    breaks: false,
    linkify: true,
    typographer: true
  };

  const md = markdownIt(mdOptions)
    .use(markdownItAttrs)
    .use(markdownItAnchor, {
      permalink: markdownItAnchor.permalink.headerLink(),
      slugify: s => s.toLowerCase().replace(/[^\w]+/g, '-')
    });

  // Custom container for :::homework, :::exercise, etc.
  const componentTypes = ['homework', 'exercise', 'prompt', 'example', 'exam', 'project'];

  componentTypes.forEach(type => {
    md.use(markdownItContainer, type, {
      validate: function(params) {
        return params.trim().match(new RegExp(`^${type}\\s*(.*)$`));
      },
      render: function(tokens, idx) {
        const token = tokens[idx];
        if (token.nesting === 1) {
          // Opening tag - parse attributes
          const match = token.info.trim().match(new RegExp(`^${type}\\s*(.*)$`));
          const attrsStr = match ? match[1] : '';
          const attrs = parseAttributes(attrsStr);
          const attrsHtml = Object.entries(attrs)
            .map(([k, v]) => `data-${k}="${v}"`)
            .join(' ');
          return `<div class="component component--${type}" ${attrsHtml}>\n`;
        } else {
          // Closing tag
          return '</div>\n';
        }
      }
    });
  });

  eleventyConfig.setLibrary("md", md);

  // ============================================
  // Passthrough Copy
  // ============================================

  // Copy CSS
  eleventyConfig.addPassthroughCopy({ "src/css": "css" });

  // Copy fonts
  eleventyConfig.addPassthroughCopy({ "src/fonts": "fonts" });

  // Copy images from content
  eleventyConfig.addPassthroughCopy("clase/**/*.{png,jpg,jpeg,gif,svg,webp}");

  // ============================================
  // Filters
  // ============================================

  // Format date in Spanish
  eleventyConfig.addFilter("formatDate", function(date) {
    if (!date) return '';
    const d = new Date(date);
    return d.toLocaleDateString('es-MX', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  });

  // Extract title from filename if no frontmatter
  eleventyConfig.addFilter("titleFromFilename", function(filename) {
    if (!filename) return 'Sin titulo';
    // Remove extension and path
    const name = filename.split('/').pop().replace(/\.\w+$/, '');
    // Remove numeric prefix (00_, 01_, etc.)
    const withoutPrefix = name.replace(/^\d+[_-]?/, '');
    // Convert underscores/hyphens to spaces and capitalize
    return withoutPrefix
      .replace(/[_-]/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  });

  // Get reading order from filename prefix
  eleventyConfig.addFilter("getOrder", function(filename) {
    if (!filename) return 999;
    const match = filename.match(/^(\d+)/);
    return match ? parseInt(match[1], 10) : 999;
  });

  // ============================================
  // Collections
  // ============================================

  // All content pages
  eleventyConfig.addCollection("content", function(collectionApi) {
    return collectionApi.getFilteredByGlob("clase/**/*.md")
      .filter(item => !item.inputPath.includes('b_libros'))
      .sort((a, b) => {
        const orderA = a.data.order || getOrderFromPath(a.inputPath);
        const orderB = b.data.order || getOrderFromPath(b.inputPath);
        return orderA - orderB;
      });
  });

  // ============================================
  // Shortcodes
  // ============================================

  // Icon shortcode (using simple text icons, no dependencies)
  eleventyConfig.addShortcode("icon", function(name) {
    const icons = {
      homework: '[T]',
      exercise: '[E]',
      prompt: '[>]',
      example: '[*]',
      exam: '[!]',
      project: '[P]',
      copy: '[C]',
      check: '[v]',
      arrow: '>'
    };
    return icons[name] || `[${name}]`;
  });

  // ============================================
  // Global Data - Default Layout
  // ============================================

  // Set default layout for all markdown files
  eleventyConfig.addGlobalData("layout", "layouts/base.njk");

  // ============================================
  // BrowserSync Configuration (for Docker)
  // ============================================

  eleventyConfig.setBrowserSyncConfig({
    host: "0.0.0.0",
    open: false,
    ui: false
  });

  // ============================================
  // Configuration
  // ============================================

  return {
    dir: {
      input: "clase",
      includes: "../uu_framework/eleventy/_includes",
      data: "../uu_framework/eleventy/_data",
      output: "_site"
    },
    templateFormats: ["md", "njk", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    pathPrefix: "/ia_p26/"
  };
};

// ============================================
// Helper Functions
// ============================================

/**
 * Parse attributes from string like {id="foo" title="bar"}
 */
function parseAttributes(str) {
  const attrs = {};
  if (!str) return attrs;

  // Match key="value" or key='value' patterns
  const regex = /(\w+)=["']([^"']+)["']/g;
  let match;
  while ((match = regex.exec(str)) !== null) {
    attrs[match[1]] = match[2];
  }
  return attrs;
}

/**
 * Get sort order from file path based on numeric prefix
 */
function getOrderFromPath(path) {
  const parts = path.split('/');
  let order = 0;

  parts.forEach((part, i) => {
    const match = part.match(/^(\d+)/);
    if (match) {
      // Weight earlier path segments more heavily
      order += parseInt(match[1], 10) * Math.pow(100, parts.length - i);
    }
  });

  return order;
}
