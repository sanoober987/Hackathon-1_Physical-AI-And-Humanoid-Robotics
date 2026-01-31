import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', 'a0b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', 'aa6'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '134'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'e2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '6b2'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '061'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '97c'),
    exact: true
  },
  {
    path: '/assistant',
    component: ComponentCreator('/assistant', '462'),
    exact: true
  },
  {
    path: '/chat',
    component: ComponentCreator('/chat', '289'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '3b0'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '51a'),
        exact: true
      },
      {
        path: '/docs/chapters/capstone-project',
        component: ComponentCreator('/docs/chapters/capstone-project', 'f31'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/chapter1',
        component: ComponentCreator('/docs/chapters/chapter1', 'b3f'),
        exact: true
      },
      {
        path: '/docs/chapters/chapter2',
        component: ComponentCreator('/docs/chapters/chapter2', '78d'),
        exact: true
      },
      {
        path: '/docs/chapters/chapter3',
        component: ComponentCreator('/docs/chapters/chapter3', '672'),
        exact: true
      },
      {
        path: '/docs/chapters/gazebo-digital-twin',
        component: ComponentCreator('/docs/chapters/gazebo-digital-twin', 'bca'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/humanoid-robotics',
        component: ComponentCreator('/docs/chapters/humanoid-robotics', '565'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/introduction-to-physical-ai',
        component: ComponentCreator('/docs/chapters/introduction-to-physical-ai', '8de'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/nvidia-isaac-brain',
        component: ComponentCreator('/docs/chapters/nvidia-isaac-brain', 'f18'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/ros2-nervous-system',
        component: ComponentCreator('/docs/chapters/ros2-nervous-system', '466'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/chapters/vision-language-action',
        component: ComponentCreator('/docs/chapters/vision-language-action', '462'),
        exact: true,
        sidebar: "tutorialSidebar"
      },
      {
        path: '/docs/intro',
        component: ComponentCreator('/docs/intro', 'aed'),
        exact: true,
        sidebar: "tutorialSidebar"
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', 'd98'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
