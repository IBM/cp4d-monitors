module.exports = {
  siteMetadata: {
    title: 'Cloud Pak Deployer Monitors',
    description: 'A Gatsby theme for the carbon design system',
    keywords: 'monitor,deployer,cp4d',
  },
  pathPrefix: `/IBM/cp4d-monitors`,
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
            'https://github.com/IBM/cp4d-monitors',
          subDirectory: '',
          branch: 'main',
        },
      },
    },
  ],
};
