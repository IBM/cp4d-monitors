import React from 'react';
import ResourceLinks from 'gatsby-theme-carbon/src/components/LeftNav/ResourceLinks';

const links = [
  {
    title: 'Cloud Pak Deployer Monitor GitHub',
    href: 'https://github.com/IBM/cp4d-monitors',
  },
  {
    title: 'Carbon',
    href: 'https://www.carbondesignsystem.com',
  },
  {
    title: 'Gatsby Guide',
    href: 'https://gatsby-theme-carbon.now.sh/getting-started',
  }
];

// shouldOpenNewTabs: true if outbound links should open in a new tab
const CustomResources = () => <ResourceLinks shouldOpenNewTabs links={links} />;

export default CustomResources;
