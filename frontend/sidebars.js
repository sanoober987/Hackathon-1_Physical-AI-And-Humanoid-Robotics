// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Chapters',
      items: [
        'chapters/introduction-to-physical-ai',
        'chapters/ros2-nervous-system',
        'chapters/gazebo-digital-twin',
        'chapters/nvidia-isaac-brain',
        'chapters/vision-language-action',
        'chapters/humanoid-robotics',
        'chapters/capstone-project'
      ],
    },
  ],
};

module.exports = sidebars;
