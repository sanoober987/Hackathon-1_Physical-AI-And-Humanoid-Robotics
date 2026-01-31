import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/assistant',
    component: ComponentCreator('/assistant', 'efe'),
    exact: true
  },
  {
    path: '/chat',
    component: ComponentCreator('/chat', 'aac'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', 'd6f'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '51f'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'aa8'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', '0ee'),
                exact: true
              },
              {
                path: '/docs/chapters/capstone-project',
                component: ComponentCreator('/docs/chapters/capstone-project', '423'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/chapter1',
                component: ComponentCreator('/docs/chapters/chapter1', '1f4'),
                exact: true
              },
              {
                path: '/docs/chapters/chapter2',
                component: ComponentCreator('/docs/chapters/chapter2', '87b'),
                exact: true
              },
              {
                path: '/docs/chapters/chapter3',
                component: ComponentCreator('/docs/chapters/chapter3', 'f4a'),
                exact: true
              },
              {
                path: '/docs/chapters/gazebo-digital-twin',
                component: ComponentCreator('/docs/chapters/gazebo-digital-twin', 'e70'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/humanoid-robotics',
                component: ComponentCreator('/docs/chapters/humanoid-robotics', '1ca'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/introduction-to-physical-ai',
                component: ComponentCreator('/docs/chapters/introduction-to-physical-ai', '42b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/nvidia-isaac-brain',
                component: ComponentCreator('/docs/chapters/nvidia-isaac-brain', '9d0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/ros2-nervous-system',
                component: ComponentCreator('/docs/chapters/ros2-nervous-system', '6ab'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/chapters/vision-language-action',
                component: ComponentCreator('/docs/chapters/vision-language-action', 'af9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', '61d'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '070'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
