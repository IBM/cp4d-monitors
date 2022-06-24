module.exports = {
  siteMetadata: {
    title: 'Cloud Pak Deployer Monitors',
    description: 'A Gatsby theme for the carbon design system',
    keywords: 'monitor,deployer,cp4d',
  },
  pathPrefix: `/CloudPakDeployer/cloud-pak-deployer-monitors`,
  plugins: [
    {
      resolve: 'gatsby-plugin-manifest',
      options: {
        name: 'Carbon Design Gatsby Theme',
        icon: 'src/images/favicon.svg',
        short_name: 'Gatsby Theme Carbon3',
        start_url: '/',
        display: 'browser',
      },
    },
    {
      resolve: 'gatsby-theme-carbon',
      options: {
        mediumAccount: 'carbondesign',
        repository: {
          baseUrl:
            'https://github.ibm.com/CloudPakDeployer/cloud-pak-deployer-monitors',
          subDirectory: '',
          branch: 'main',
        },
      },
    },
  ],
};
