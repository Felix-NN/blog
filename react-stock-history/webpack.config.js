const webpack = require('webpack');
const config = {
    entry:  __dirname + '/src/index.js',
    output: {
        path: __dirname + '/dist',
        filename: 'bundle.js',
    },
    resolve: {
        extensions: ['.js', '.jsx', '.css']
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
              }        
        ]
    }
};
module.exports = config;