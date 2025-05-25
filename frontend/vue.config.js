const { defineConfig } = require('@vue/cli-service')
const CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  chainWebpack: (config) => {
    config.plugins.delete("copy"); // Отключает copy-webpack-plugin
  },
};
