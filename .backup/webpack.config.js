const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');


const Assets = [
  '@hotwired/turbo/dist/turbo.es2017-esm.js'
]

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    clean: true,
    path: path.resolve(__dirname, 'app/static/dist/js'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.js$/i, include: path.resolve(__dirname, 'src'),
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env'],
          },
        },
      },
      {
        test: /\.css$/i,
        include: path.resolve(__dirname, 'src'),
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  }
};