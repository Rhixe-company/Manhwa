const { merge } = require("webpack-merge");
const commonConfig = require("./common.config");

// This variable should mirror the one from config/settings/production.py
const s3BucketName = process.env.DJANGO_AWS_STORAGE_BUCKET_NAME;
const awsS3Domain = process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN ? process.env.DJANGO_AWS_S3_CUSTOM_DOMAIN : `${s3BucketName}.s3.amazonaws.com`;
const staticUrl = `https://${awsS3Domain}/static/`;
const staticUrl1 = "/static/";
module.exports = merge(commonConfig, {
  mode: "production",
  devtool: "source-map",
  performance: { hints: false },
  bail: true,
  output: {
    publicPath: `${staticUrl1}webpack_bundles/`,
  },
});
