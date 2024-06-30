const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack");
const WindiCSSWebpackPlugin = require("windicss-webpack-plugin");

module.exports = {
  target: ["web"],
  context: path.join(__dirname, "../"),
  entry: {
    index: path.resolve(__dirname, "../", "src", "index"),
    vendors: path.resolve(__dirname, "../", "src", "vendors"),
    chapters: path.resolve(__dirname, "../", "src", "chapters"),
    search: path.resolve(__dirname, "../", "src", "search"),

    // modal: path.resolve(__dirname, "../", "src", "modal"),
    // drawer: path.resolve(__dirname, "../", "src", "drawer"),
  },
  output: {
    path: path.resolve(__dirname, "../", "dist", "webpack_bundles"),
    publicPath: "/static/webpack_bundles/",
    filename: "js/[name]-[fullhash].js",
    chunkFilename: "js/[name]-[hash].js",
    clean: true,
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
    }),
    new BundleTracker({
      path: path.resolve(path.join(__dirname, "../", "dist")),
      filename: "webpack-stats.json",
    }),
    new MiniCssExtractPlugin({
      filename: "css/[name].[contenthash].css",
    }),
    new WindiCSSWebpackPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: "ts-loader",
        exclude: /node_modules/,
      },
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
      {
        test: /\.s?css$/i,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: ["postcss-preset-env", "autoprefixer", "pixrem"],
              },
            },
          },
          "sass-loader",
        ],
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/,
        type: "asset/resource",
      },
    ],
  },
  resolve: {
    modules: ["node_modules"],
    extensions: [".tsx", ".ts", ".js", ".jsx", "..."],
  },
  optimization: {
    minimize: true,
    splitChunks: {
      chunks: "async",
      minSize: 20000000,
      minRemainingSize: 0,
      minChunks: 1,
      maxAsyncRequests: 60,
      maxInitialRequests: 60,
      enforceSizeThreshold: 50000000,
      // cacheGroups: {
      //   defaultVendors: {
      //     filename: "js/[name]-[contenthash].js",
      //     test: /[\\/]node_modules[\\/]/,
      //     name: "ven",
      //     chunks: "all",
      //     priority: -10,
      //     reuseExistingChunk: true,
      //   },
      //   commons: {
      //     filename: "js/[name]-[contenthash].js",
      //     test: /[\\/]node_modules[\\/]/,
      //     name: "vendor",
      //     chunks: "all",
      //     priority: -10,
      //     reuseExistingChunk: true,
      //   },
      // },
    },
  },
};
