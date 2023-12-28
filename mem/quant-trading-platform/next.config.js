// next.config.js
const path = require('path');

module.exports = {
  reactStrictMode: true, // 开启严格模式
  env: {
    // 在这里可以添加环境变量
    NEXT_PUBLIC_API_BASE_URL: process.env.NEXT_PUBLIC_API_BASE_URL,
  },
  sassOptions: {
    // 如果你使用Sass，可以在这里配置Sass选项
    includePaths: [path.join(__dirname, 'styles')],
  },
  images: {
    // 如果你使用next/image，可以在这里配置图像域
    domains: ['example.com'],
  },
  // 如果你需要重写webpack配置
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // 注意：不要修改输入参数的引用，例如 `config`
    // 举个例子，添加一个别名
    config.resolve.alias['@'] = path.join(__dirname, '.');

    // 重要：返回修改后的配置
    return config;
  },
  // 其他 Next.js 配置选项...
};