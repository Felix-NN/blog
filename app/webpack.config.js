const webpack = require('webpack');
const config = {
    entry:  __dirname + '/static/src/index.js',
    resolve: {
        extensions: ['.js', '.jsx', '.css']
    },
    output: {
        path: __dirname + '/static/dist',
        filename: 'bundle.js',
    },
    module: {
        rules: [
            {
            test: /\.(js|jsx)?/,
            exclude: /node_modules/,
            loader: 'babel-loader',
            options: {
                presets: ['@babel/preset-env',
                  '@babel/react',{
                  'plugins': ['@babel/plugin-proposal-class-properties']}]
            }
         },   {
                test: /\.css$/,
                use: ['style-loader', 'css-loader'],
              },
              {
                test: /\.(png|jpg|gif|svg|eot|ttf|woff|woff2)$/,
                loader: 'url-loader',
                options: {
                  limit: 10000
                }
            }
        ]
    }
};
module.exports = config;