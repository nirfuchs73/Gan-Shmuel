module.exports = {
  devServer: {
    // proxy: {
    //   '/health$': {
    //     // target: 'http://ec2-54-211-161-133.compute-1.amazonaws.com:8090/health',
    //     target: 'http://localhost:8090/health',
    //     changeOrigin: true,
    //     // router: {
    //     //   'http://localhost:8080/': 'http://localhost:8090/',
    //     //   'http://localhost:8090/': 'http://localhost:8090/',
    //     // },
    //   },
    // },
    proxy: 'http://localhost:8090/',
  },
};
