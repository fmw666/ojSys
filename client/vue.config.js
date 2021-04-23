module.exports = {
    publicPath: '/',
    outputDir: 'dist',
    assetsDir: 'static',
    lintOnSave: false,
    runtimeCompiler: false,
    productionSourceMap: false,

    devServer: {
        host: 'localhost',
        port: 3000,
        https: false,
        proxy: {
          '/api': {
            // 测试环境
            target: 'http://127.0.0.1:8000/api/v1/', // 接口域名
            //secure: false, // 如果是https接口，需要配置这个参数
            changeOrigin: true, // 是否跨域
            ws: true,
            pathRewrite: {
              '^/api': ''  // 需要rewrite重写的
            }
          }
        },
    },
}