// @ts-check
// Docusaurus configuration for Physical AI & Humanoid Robotics

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Comprehensive Textbook on Physical AI and Humanoid Robotics',
  favicon: 'img/favicon.ico',

  url: 'https://physicalai-book.com', // Production URL
  baseUrl: '/',

  organizationName: 'physicalai-book', // GitHub org/user
  projectName: 'physicalai-book', // Repo name

  onBrokenLinks: 'warn', // avoid build failure
  markdown: {
    format: 'detect',
    mermaid: false,
    mdx1Compat: {
      comments: true,
      admonitions: true,
      headingIds: true,
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'], // Removed Urdu language support
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Options for the docs plugin
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Route base path for docs
          routeBasePath: '/docs',
          // Path to the docs folder relative to website dir
          path: 'docs',
          // Include current docs and translated docs
          includeCurrentVersion: true,
        },
        blog: {
          showReadingTime: true,
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      require.resolve('@docusaurus/plugin-client-redirects'),
      {
        fromExtensions: ['html'],
        redirects: [],
      },
    ],
  ],

  themeConfig: /** @type {import('@docusaurus/preset-classic').ThemeConfig} */ ({
    image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Physical AI & Humanoid Robotics',
      logo: {
        alt: 'Physical AI Logo',
        src: 'img/logo.svg',
        width: 32,
        height: 32,
      },
      items: [
        {
          to: '/',
          label: 'Home',
          position: 'left',
        },
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Textbook',
        },
        {
          to: '/assistant',
          label: 'AI Assistant',
          position: 'left',
        },
        {
          href: 'https://github.com/physicalai-book/physicalai-book',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            { label: 'Tutorial', to: '/docs/intro' },
          ],
        },
        {
          title: 'Resources',
          items: [
            { label: 'GitHub', href: 'https://github.com/physicalai-book/physicalai-book' },
            { label: 'Documentation', to: '/docs/intro' },
          ],
        },
        {
          title: 'Community',
          items: [
            { label: 'Physical AI Community', href: 'https://example.com/community' },
            { label: 'Robotics Forum', href: 'https://example.com/forum' },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook, Inc. Built with Docusaurus.`,
    },
    prism: {
      theme: lightCodeTheme,
      darkTheme: darkCodeTheme,
      additionalLanguages: ['python', 'bash', 'json', 'yaml', 'docker'],
    },
  }),
};

module.exports = config;
